# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides features to process a task.
"""
import abc
import os
import time
import traceback
from pathlib import Path
import pandas as pd

from constant import Constant, Message
import utility
from utility import get_length
from progress_status import ProgressStatus
import logger
from telemetry_logger import log_error
from progress_store import ProgressStore
from score_wrapper import ScoreWrapper
from task_result import TaskResult
from task_manager import TaskManager
from run_context_factory import RunContextFactory


class TaskProcessor:
    """ Provides features to process a task.
        call the init() in the entry script one time if there is any task picked by the current process.
    """

    def __init__(self, args):
        self.logger = logger.get_logger()
        self.run_context = RunContextFactory.get_context()
        self.args = args

        self.ip_address = utility.get_ip()

        # Initialize counters
        self.task_time = 0
        self.task_process_time = 0

        self.total = 0
        self.succeeded = 0
        self.run_method_time = 0

        self.score_wrapper = ScoreWrapper(self.args.scoring_module_name)
        self.progress_store = ProgressStore()
        self.task_manager = TaskManager(args)

    def __reduce__(self):
        return (self.__class__, (self.args,))

    @abc.abstractmethod
    def validate(self, score_output):
        """ Validate output from scoring.run()."""

    @abc.abstractmethod
    def get_inputs(self, task):
        """ Get inputs from a task."""

    def append_to_temp_file(self, score_output):
        """ Append result from run() to the temp file owned by the current process.
            If the score_output is empty, the result will be an empty file with file size zero.
        """
        if not isinstance(score_output, list) and not isinstance(score_output, pd.DataFrame):
            raise Exception(f"The type of return value is not a list or dataframe: {score_output}.")

        output_path = self.args.output
        Path(output_path).mkdir(parents=True, exist_ok=True)

        output_file = os.path.join(
            output_path, f"temp_{self.ip_address}_{os.getpid()}_{self.args.append_row_file_name}"
        )

        if isinstance(score_output, list):
            with open(output_file, "a") as fil:
                for prediction_data in score_output:
                    fil.write("{}\n".format(prediction_data))
                    fil.flush()
            self.logger.debug(f"write {len(score_output)} files' prediction results to {output_file}.")
        else:
            score_output.to_csv(output_file, header=None, index=None, sep=" ", mode="a")

    def process_mini_batch(self, inputs):
        """ Process a mini batch.
            :param list inputs:
                A list of paths to files **OR** a pandas dataframe
            :rtype: int, the number of succeeded items.
        """
        self.run_method_time = 0

        score_output = []
        start_timestamp = utility.timestamp()

        self.logger.debug(f"scoring {inputs} with output_action='{self.args.output_action}'")
        if self.args.output_action == "summary_only":
            scoring_start = time.perf_counter()
            score_output = self.score_wrapper.run(inputs)
            self.run_method_time = time.perf_counter() - scoring_start
            self.validate(score_output)

            self.logger.debug(f"ScoreWrapper {inputs} end. succeeded: {score_output}.")

        elif self.args.output_action == "append_row":
            scoring_start = time.perf_counter()
            score_output = self.score_wrapper.run(inputs)
            self.validate(score_output)
            self.run_method_time = time.perf_counter() - scoring_start
            self.append_to_temp_file(score_output)

        output_count = get_length(score_output)
        if output_count <= self.total:
            self.succeeded = output_count
        else:
            self.succeeded = self.total  # Cap the succeeded count by the total.
            self.logger.warning(
                f"run() returned {output_count} items, which is more than input count {self.total}."
                " Using the input count as succeeded count and continue."
                f" Please check run() method in your entry script. The mini batch is {inputs}."
            )

        self.logger.debug(
            f"Batch processing completed. Total count: {self.total}, success count: {self.succeeded}, "
            f"processing time: {utility.timestamp()-start_timestamp}, run method time: {str(self.run_method_time)}"
        )

    def notify_progress(
        self, id, dequeue_count, total, succeeded, start_time, duration, process_time, run_method_time, status
    ):  # pylint: disable=invalid-name,redefined-builtin
        """ Notify progress to the master.
        """
        task_result = TaskResult(
            id=id,
            dequeue_count=dequeue_count,
            total=total,
            succeeded=succeeded,
            failed=total - succeeded,
            ip=self.ip_address,
            pid=os.getpid(),
            start_time=start_time,
            duration=duration,
            process_time=process_time,
            run_method_time=run_method_time,
            status=status,
        )

        self.progress_store.notify_progress(task_result)

    def finish_task(self, task, total, succeeded, start_time, duration, process_time, run_method_time):
        """ Notify the master that a task is processed and delete the task from the pending queue
        """
        try:
            # If this failed, the message will be picked up and processed again
            status = ProgressStatus.TASK_PROCESSED
            self.notify_progress(
                task.id,
                task.dequeue_count,
                total,
                succeeded,
                start_time,
                duration,
                process_time,
                run_method_time,
                status,
            )
            # Remove the item from queue after every thing is done.
            self.task_manager.delete_task(task)
        except BaseException as exc:
            message = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format(
                f"finish task {task.to_json()}", exc, traceback.format_exc()
            )
            self.logger.error(message)
            raise exc

    def process_task(self, task):
        """ Process a task.
            :param Task task, the task to process.
        """

        try:
            start_time = utility.timestamp()
            process_time_start = time.process_time()

            status = ProgressStatus.TASK_PICKED
            self.notify_progress(task.id, task.dequeue_count, 0, 0, start_time, 0, 0, 0, status)

            inputs = self.get_inputs(task)

            self.total = get_length(inputs)

            self.succeeded = 0
            self.process_mini_batch(inputs)

            duration = utility.timestamp() - start_time
            process_time = time.process_time() - process_time_start
            self.finish_task(
                task, self.total, self.succeeded, start_time, duration, process_time, self.run_method_time
            )
        finally:
            self.task_time = utility.timestamp() - start_time
            self.task_process_time = time.process_time() - process_time_start
