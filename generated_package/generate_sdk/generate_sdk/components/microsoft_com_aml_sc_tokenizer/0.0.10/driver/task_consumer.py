# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides task consumer to process tasks.
"""
import os
import sys
import traceback
from pathlib import Path
from multiprocessing import current_process
from azureml._base_sdk_common import _ClientSessionId

from constant import Constant, Message
from run_context_factory import RunContextFactory
from job_state import JobState
import logger
from telemetry_logger import log_info, log_warning, log_error, log_process_telemetry
from log_config import LogConfig
from task_manager import TaskManager
from event import Event
from processor_factory import ProcessorFactory
from utility import get_ip, fmt_time, timestamp


class TaskConsumer:
    """ Define a task consumer to get tasks from the task manager and pass the task to a task processor."""

    FAILED_TASK_COUNT_TO_STOP = 10

    def __init__(self, args):
        self.logger = logger.get_logger()
        self.args = args
        self.run_context = RunContextFactory.get_context()
        self.visibility_timeout = args.run_invocation_timeout + args.task_overhead_timeout

        self.task_manager = TaskManager(args)
        self.task_processor = ProcessorFactory(args).get_processor()
        self.job_state = JobState()
        self.current_task = None  # Only one task will be processed at a moment.

        self.on_tick = Event()  # notity this is moving on

        self.exceptions = []

        # Initialize counters
        self.start_time = timestamp()

        # For all processed tasks in this process
        self.total_run_method_time = 0
        self.total_task_time = 0
        self.total_task_process_time = 0

        self.total_items = 0  # Total mini batch items processed by this process.
        self.succeeded_items = 0

        self.task_picked = 0  # Total tasks processed by this process.
        self.task_finished = 0  # include succeeded and failed
        self.task_succeeded = 0  # Succeeded tasks processed by this process.

        self.scoring_init_failed = False  # Will change to True if scoring init() failed.
        self.scoring_init_done = False  # Will change to True after scoring init() returned
        self.scoring_run_done = False  # Will change to True after scoring run() returned

        # None: running, 0: finished,
        self.exitcode = None

    def get_current_task_id(self):
        """ Get current task id."""
        task_id = -1

        task = self.current_task
        if task:
            task_id = task.id

        return task_id

    def process_task(self, task):
        """ Process a task.
            :param Task task, the task to process.
        """
        self.on_tick()

        try:
            self.scoring_run_done = False
            self.task_picked += 1
            self.task_processor.process_task(task)
            self.task_succeeded += 1
        except BaseException as exc:
            self.task_manager.renew_task_lease(task, 0)  # Change the task to be visible immediately.
            # Swallow all exception to move to next task
            message = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format(
                f"Failed to process task {task.to_json()}", exc, traceback.format_exc()
            )
            log_error(message)
            self.exceptions.append(exc)
        finally:
            self.scoring_run_done = True
            sys.stdout.flush()
            self.task_finished += 1
            self.total_run_method_time += self.task_processor.run_method_time
            self.total_task_time += self.task_processor.task_time
            self.total_task_process_time += self.task_processor.task_process_time
            self.total_items += self.task_processor.total
            self.succeeded_items += self.task_processor.succeeded

    def redirect_stdout(self):
        """ Redirect stdout to file.

            As we catch the exception from entry script, it won't write error to stderr.
            So we don't redirect stderr.
        """

        log_dir = Path(LogConfig().log_dir) / "user"
        ip_addr = get_ip()
        if ip_addr:
            log_dir /= ip_addr

        log_dir.mkdir(parents=True, exist_ok=True)
        stdout_file = str(Path(log_dir) / f"{current_process().name}.stdout.txt")

        sys.stdout = open(stdout_file, "w")

    def process_tasks(self):
        """ Loop to fetch and process task until:
                1. Gets an empty task list from the task manager for:
                    a) no visible task anymore.
                    b) the task manager gets stop signal from the master.
                2. Run into any exception.
        """
        try:
            self.task_processor.score_wrapper.init()
        except BaseException as exc:  # notify the process to exit
            self.scoring_init_failed = True
            raise exc
        finally:
            self.scoring_init_done = True

        self.on_tick()  # tick one time after init()

        while True:
            tasks = self.task_manager.get_tasks(self.visibility_timeout)
            if not tasks:
                log_info(f"This worker is exiting since get_tasks did not returned tasks.")
                self.task_processor.score_wrapper.shutdown()
                break

            for task in tasks:
                self.logger.debug(f"Got task {task.id}.")

                self.current_task = task
                self.process_task(task)

            if self.need_exit():
                break

    def need_exit(self):
        """ Check if the process need to exit.
            If it matches the conditions, set exit code and return True.
        """
        if self.scoring_init_failed:
            self.exitcode = Constant.EXIT_CODE_SCORE_INIT_FAILED
            return True

        task_failed = self.task_finished - self.task_succeeded
        if task_failed > self.FAILED_TASK_COUNT_TO_STOP:
            log_warning(
                f"{task_failed} {Constant.TERM_MINI_BATCHES} failed. {self.task_succeeded} succeeded."
                "This process is exiting and a new process will start."
            )
            if self.task_succeeded == 0:
                self.exitcode = Constant.EXIT_CODE_SCORE_RUN_ALL_FAILED
            else:
                self.exitcode = Constant.EXIT_CODE_SCORE_RUN_SOME_FAILED

            return True

        return False

    def cd_temp(self):
        """ Change to local temp folder dedicate for the current process.
            This is to make sure that get_model_path don’t download model into a shared directory.
        """
        temp_dir = self.run_context.temp_dir
        self.logger.debug(f"change to dir: {temp_dir}.")
        os.chdir(temp_dir)

    def _start(self, number):
        """ This is the working method in a process.
            :param int number, the order of the process.
        """
        LogConfig().config(self.args.logging_level, is_master=False)  # config for new process
        self.logger = logger.get_logger()
        log_info(f"Process tasks on process {number}.")
        log_info(f"DatasetLog - ClientSessionId: {_ClientSessionId}")

        self.on_tick()

        self.cd_temp()  # change to local folder, don't use a shared storage.

        try:
            old_stdout = sys.stdout
            self.redirect_stdout()
            self.process_tasks()
        finally:
            sys.stdout.close()
            sys.stdout = old_stdout
            now = timestamp()
            log_process_telemetry(
                start_time=self.start_time,
                end_time=now,
                duration=now - self.start_time,
                process_time=self.total_task_process_time,
                run_method_time=self.total_run_method_time,
                total_tasks=self.task_picked,
                succeeded_tasks=self.task_succeeded,
                total_items=self.total_items,
                succeeded_items=self.succeeded_items,
            )

    def get_profile_filename(self):
        """Return the filename for profile output."""
        log_dir = LogConfig().log_dir
        profile_dir = Path(log_dir) / f"sys/worker/{get_ip()}/"
        profile_dir.mkdir(parents=True, exist_ok=True)
        return str(profile_dir / f"{current_process().name}.task_consumer.profile")

    def start(self, number):
        """If profiling_module specified, call _start() with profile.
            Or call _start() directly.
        """
        module = self.args.profiling_module
        if module:
            from profile_wrapper import ProfileWrapper

            ProfileWrapper(module).runctx(
                "self._start(number)", globals(), locals(), filename=self.get_profile_filename()
            )
        else:
            self._start(number)
