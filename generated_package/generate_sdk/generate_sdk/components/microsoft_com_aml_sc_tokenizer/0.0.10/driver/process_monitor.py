# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides process monitor features.
"""
import time
import traceback
from multiprocessing import Process
from multiprocessing import current_process

import logger
from constant import Constant, Message
from job_state import JobState
from telemetry_logger import log_info, log_warning, log_error
from process_helper import ProcessHelper
from utility import get_available_gpu_count


class ProcessMonitor:
    """ The class monitors processes and starts a new process if a process has exitcode > 0

        There must be exact one instance of this class on non-master nodes.
        If master node also starts worker, there also must be exact one instance of this class on it.
        The instance is running in the main process.

        About exitcode :
        The child’s exit code.
        This will be None if the process has not yet terminated.
        Zero, the process ends without error.
        A negative value -N indicates that the child was terminated by signal N.
        Reference: https://docs.python.org/3.7/library/multiprocessing.html#multiprocessing.Process.exitcode
    """

    # TODO: Define more codes or a range to restart
    # Such as starting one excepting SIGTERM
    POLLING_INTERVAL = 10

    def __init__(self):
        self.logger = logger.get_logger()

        if current_process().name == "MainProcess":
            self.processes = []
            self.new_process_target = None
            self.new_process_args = ()
            self.new_process_count = 0
            self.new_process_assigned_gpu_index = 0
            self.new_process_assigned_gpu_index_mapping = {}
            self.stopping = False
            self.process_helper = ProcessHelper()
            self.job_state = JobState()
            self.total_started = 0

    def __reduce__(self):
        """ Declare what to pickle.
        """
        return (self.__class__, ())

    def get_new_process_args(self):
        """ Return a new args by increasing the first parameter, which is considered as the index of the process.
        """
        if self.new_process_args:
            # Consider the first item as index if it's an integer.
            _list = list(self.new_process_args)
            if isinstance(_list[0], int):
                _list[0] += self.new_process_count
            if len(self.new_process_args) > 1 and isinstance(_list[1], int):
                _list[1] += self.new_process_assigned_gpu_index
            return tuple(_list)

        return self.new_process_args

    def start_process(self):
        """ Start and return a new process.
            Wait until the new process is alive or timeout.
        """
        if self.new_process_target:
            new_args = self.get_new_process_args()

            # Set daemon to True so that it won't block the main process from exiting.
            new_process = Process(target=self.new_process_target, args=new_args, daemon=True)
            try:
                time.sleep(0.1)  # This is a temp workaround. Or the process will hange on Python 3.6.9 on Linux.
                new_process.start()
                self.new_process_assigned_gpu_index_mapping[new_process.pid] = self.new_process_assigned_gpu_index
                log_info(
                    f"Start a new process with index: {self.new_process_count}, pid: {new_process.pid}, "
                    f"assigned_gpu_index: {self.new_process_assigned_gpu_index}."
                )
                self.new_process_count += 1

                gpu_count = get_available_gpu_count()
                if gpu_count > 0:
                    self.new_process_assigned_gpu_index += 1
                    self.new_process_assigned_gpu_index %= gpu_count
                return new_process
            except BaseException as exc:
                log_warning(
                    f"Start the new process {self.new_process_count} failed with {exc}.\n{traceback.format_exc()}"
                    " In next round of checking, the process monitor will try to start another to replace this one."
                    " Swallow the exception to continue."
                )

        return None

    def start_processes(self, total):
        """ Create and start processes.
            :total, the total number of processes to start.
        """
        if not self.stopping:
            for _ in range(total):
                new_process = self.start_process()
                self.processes.append(new_process)
                self.total_started += 1

    def check(self):
        """ The method checks the health of processes:
            1. Kill not alive process if it doesn't end.
            2. If a process ends with exit code, check if the exit code is in the list to start a new one.
                Start a new process if the code is in the list.
            3. Update self.processes to a list of running processes.
        """
        running = []
        for proc in self.processes:
            need_to_start_process = False
            if proc.exitcode is None:  # process hasn't stopped
                if proc.is_alive():
                    running.append(proc)
                    self.logger.debug(f"The process {proc.pid} is alive.")
                else:
                    log_info(f"The process {proc.pid} is not alive. Try to kill it.")
                    self.process_helper.kill_pid(proc.pid)

                    need_to_start_process = True

            else:
                log_info(f"The process {proc.pid} exits with exitcode {proc.exitcode}.")
                if proc.exitcode in Constant.EXIT_CODES_START_NEW_PROCESS:
                    log_info(f"A new process will be started to replace the process {proc.pid}.")
                    need_to_start_process = True

            if not self.stopping and need_to_start_process:
                # Mark the GPU index in old process as available.
                self.new_process_assigned_gpu_index = self.new_process_assigned_gpu_index_mapping[proc.pid]
                new_process = self.start_process()
                if new_process:
                    running.append(new_process)

        self.processes = running

    def wait(self):
        """ Poll the status of the proceses and restart a new one for process with exitcode > 0.
            Sleep and continue to poll until all processes end without error.
        """
        try:
            while self.processes:
                self.check()

                self.logger.debug(f"Running processes {self.processes}.")

                if not self.stopping:
                    if self.job_state.stopping():
                        self.logger.info(Message.GOT_STOP_SIGNAL)
                        self.stopping = True

                self.logger.debug(f"stopping: {self.stopping}.")

                # As we don't use a lock for self.processes, sleep before stop_processes()
                # so that new process can be in self.processes in racing case.
                time.sleep(self.POLLING_INTERVAL)

                if self.stopping:
                    self.stop_processes()
                    break
        except BaseException as exc:
            log_error(f"The process monitor failed with error {exc}. Detail {traceback.format_exc()}.")
            raise exc
        finally:
            log_info(f"The process monitor exits.")

    def stop_processes(self):
        """ Stop all processes use kill().
        """
        self.logger.debug(f"Try to stop processes {self.processes}.")
        for proc in self.processes:
            self.logger.debug(f"kill process {proc}.")
            self.process_helper.kill_pid(proc.pid)

    def signal_stop(self):
        """ Don't start new process and stop all running ones
        """
        log_info(f"Try to stop processes {self.processes}.")
        self.stopping = True
        self.stop_processes()
        log_info(f"Stopped processes {self.processes}.")
