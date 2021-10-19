# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This is worker module.

This module provides worker implemetation to process tasks.
"""
from pathlib import Path
import multiprocessing as mp
from multiprocessing import current_process
import psutil

from utility import get_ip
from log_config import LogConfig
from node import Node
from process_helper import ProcessHelper
from process_monitor import ProcessMonitor
from worker_process import WorkerProcess


class Worker(Node):
    """The class for ParallelRunStep worker node.

    A *worker* represents the worker node inside of an AmlCompute Batch Inferencing cluster.

    .. remarks::

        A *worker* represents the worker node inside of an AmlCompute Batch Inferencing cluster.
        A worker is the object used to provide the shared features of Worker node.
    """

    def __init__(self, args):
        super().__init__(args)
        assert current_process().name == "MainProcess"  # Ensure this class only runs in main process
        self.process_monitor = None

    def __reduce__(self):
        """ Declare what to pickle.
        """
        return self.__class__, ()

    def _start(self):
        """ Start processes to process tasks.
            Call wait() to wait the processes to finish.
        """
        # Increase the niceness, i.e., lower the priority, of the current process.
        # This will change the main process and all new processes.
        # The goal is to yield more resources to AmlCompute processes.
        if psutil.LINUX:
            mp.set_start_method("spawn", force=True)

        ProcessHelper().nice(nice=self.args.nice)

        self.process_monitor = ProcessMonitor()

        worker_process = WorkerProcess()
        self.process_monitor.new_process_target = worker_process.start
        self.process_monitor.new_process_args = (0, 0)

        message = f"Start worker with {self.args.process_count_per_node} processes."
        self.logger.info(message)

        self.process_monitor.start_processes(self.args.process_count_per_node)

    def get_profile_filename(self):
        """Return the filename for profile output."""
        log_dir = LogConfig().log_dir
        profile_dir = Path(log_dir) / f"sys/worker/{get_ip()}/"
        profile_dir.mkdir(parents=True, exist_ok=True)
        return str(profile_dir / f"{current_process().name}.profile")

    def start(self):
        """If profiling_module specified, call _start() with profile.
            Or call _start() directly.
        """
        module = self.args.profiling_module
        if module:
            from profile_wrapper import ProfileWrapper

            ProfileWrapper(module).runctx("self._start()", globals(), locals(), filename=self.get_profile_filename())
        else:
            self._start()

    def wait(self):
        """ Wait all working processes to finish.
            This method should be called in the process creating Worker instance.
        """
        self.process_monitor.wait()

    def signal_stop(self):
        """ Stop worker process and exit.
        """
        self.logger.debug("Stop process monitor")
        self.process_monitor.signal_stop()
