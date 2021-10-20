# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides worker process implementation to process tasks.
"""
from multiprocessing import current_process
import os
from pathlib import Path
import sys
import time
from threading import Thread
import traceback

from constant import Constant, Message
import logger
from log_config import LogConfig
from telemetry_logger import log_info, log_warning, log_error
from job_state import JobState
from progress_status import ProgressStatus
from task_consumer import TaskConsumer
from process_helper import ProcessHelper
from utility import get_available_gpu_count, get_ip
from resource_monitor import ResourceMonitor
from arg_parser import ArgParser
from job_args import JobArgs


class WorkerProcess:
    """ The class for ParallelRunStep worker process.
        A worker process has:
            1. A monitor loop in the main thread.
            2. A thread to run task processer.
        The process will exit with Constant.EXIT_CODE_PROCESS_TIMEOUT to tell the process monitor
         to start a new worker process in cases:
            1. the task processor stops with exception.
            2. timeout. This time out is based on the tick different since last one.
             So the process will stop if it hangs anywhere.
    """

    POLL_INTERVAL = 1  # in seconds

    def __init__(self):
        args = ArgParser().parse_job_args()
        self.args = JobArgs().from_namespace(args)
        self.logger = logger.get_logger()
        self.total_run_timeout = args.run_invocation_timeout + args.task_overhead_timeout

        self.job_state = JobState()
        self.task_consumer = TaskConsumer(args)
        self.worker_thread_ends = False  # set this to True on task processor exit.
        self.last_tick = time.perf_counter()

        self.task_consumer.on_tick += self.on_tick
        self.logger.debug(f"poll interval: {self.POLL_INTERVAL}, total_run_timeout: {self.total_run_timeout}")

    def __reduce__(self):
        """ Declare what to pickle.
            This is needed for Python 3.6.9, but not for 3.7.3.
            Not verified against other versions.
        """
        return (self.__class__, ())

    def on_tick(self):
        """ Event handler for the event task_consumer.on_tick.
        """
        self.last_tick = time.perf_counter()
        self.logger.debug(f"update last_tick to {self.last_tick}")

    def exit_unfinished(self, message):
        """ Exit the current process with the timeout exitcode.
            :param message, the warning message.
        """
        log_warning(message)
        if not self.task_consumer.scoring_init_done:  # init() timeout
            self.task_consumer.task_processor.score_wrapper.notify_init_progress(
                ProgressStatus.ENTRY_SCRIPT_INIT_TIMEOUT
            )
        elif not self.task_consumer.scoring_run_done:  # run() time
            task_id = self.task_consumer.get_current_task_id()
            self.task_consumer.task_processor.score_wrapper.notify_run_progress(
                task_id, ProgressStatus.ENTRY_SCRIPT_RUN_TIMEOUT
            )

        sys.exit(Constant.EXIT_CODE_PROCESS_TIMEOUT)

    def check_timeout(self):
        """ Check and exit the process if init() or run() cannot finish within the allowed duration.
        Don't check if it's not in the middle of init() or run(), such as pending on get_task()
        """
        if self.task_consumer.scoring_init_done and self.task_consumer.scoring_run_done:
            return

        now = time.perf_counter()
        total_seconds = round(now - self.last_tick)
        self.logger.debug(f"wait for {total_seconds} seconds. Perfcounter now: {now}, last: {self.last_tick}.")

        if total_seconds >= self.total_run_timeout:
            task_id = self.task_consumer.get_current_task_id()
            self.exit_unfinished(Message.PROCESS_TIMEOUT.format(task_id, self.total_run_timeout))

    def monitor(self):
        """ Exit the process if no tick within the allowed wait time.
        """
        self.logger.debug(f"monitor() starts")
        while not self.worker_thread_ends:
            if self.job_state.stopping():
                self.logger.info(Message.GOT_STOP_SIGNAL)
                break

            self.check_timeout()

            time.sleep(self.POLL_INTERVAL)

        if self.worker_thread_ends:
            if self.task_consumer.exceptions:  # stopped with error.
                task_id = self.task_consumer.get_current_task_id()
                self.exit_unfinished(Message.PROCESS_ABORTED.format(task_id))

        log_info(f"monitor() ends with self.worker_thread_ends={self.worker_thread_ends}.")

    def start_task_consumer(self, number):
        """ The target for processing thread.
            :param int number, the order of the the current process.
        """
        try:
            self.task_consumer.start(number)
        except BaseException as exc:
            self.logger.error(
                f"The task consumer thread in process {os.getpid()} failed with {exc}."
                f" Detail {traceback.format_exc()}."
            )
            raise exc
        finally:
            # Notify the main thread to stop.
            self.worker_thread_ends = True
            self.logger.info(f"The task consumer thread in process {os.getpid()} ends.")

    def start_proccessing_thread(self, number):
        """ Start a new thread to process task.
            This is a daemon thread and won't hold main thread from exiting,
            as we want to exit the process if a task exceeding the time limit.
        """
        thr = Thread(target=self.start_task_consumer, args=(number,), daemon=True)
        thr.start()

    def _start(self, number, assigned_gpu_index):
        """ Start thread to process tasks and poll the health.
            number: the seqential number to identify the worker process.
        """
        gpu_count = get_available_gpu_count()
        if gpu_count > 0 and assigned_gpu_index < gpu_count:
            os.environ["CUDA_VISIBLE_DEVICES"] = f"{assigned_gpu_index}"
            self.logger.info(f"Assign GPU {assigned_gpu_index} to worker {os.getpid()}")

        self.logger.debug(f"Process {number}: start resource monitor.")
        with ResourceMonitor(self.args.resource_monitor_interval):

            process_helper = ProcessHelper()
            pid = os.getpid()
            process_helper.write_pid(pid)  # save the pid to a file.

            try:
                log_info(f"Process {number}: start processing thread.")
                self.start_proccessing_thread(number)
                log_info(f"Process {number}: start monitor poll.")
                self.monitor()
                log_info(f"Process {number}: monitor finished.")
            except BaseException as exc:
                log_error(f"The worker process {pid} failed with {exc}. Detail {traceback.format_exc()}.")
                raise exc
            finally:
                log_info(f"The worker process {pid} exits.")
                process_helper.delete_pid(pid)  # delete the pid file.

    def get_profile_filename(self):
        """Return the filename for profile output."""
        log_dir = LogConfig().log_dir
        profile_dir = Path(log_dir) / f"sys/worker/{get_ip()}/"
        profile_dir.mkdir(parents=True, exist_ok=True)
        return str(profile_dir / f"{current_process().name}.profile")

    def start(self, number, assigned_gpu_index):
        """If profiling_module specified, call _start() with profile.
            Or call _start() directly.
        """
        module = self.args.profiling_module
        if module:
            from profile_wrapper import ProfileWrapper

            ProfileWrapper(module).runctx(
                "self._start(number, assigned_gpu_index)", globals(), locals(), filename=self.get_profile_filename()
            )
        else:
            self._start(number, assigned_gpu_index)
