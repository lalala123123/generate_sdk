# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides progress summary features on master.
"""
import logging

import logger
from constant import Constant, Message
from exception import (
    NoTaskPickedException,
    TaskPoisonedException,
    NoTaskProcessedException,
    SomeTaskProcessedException,
)
from entry_script_exception import (
    EntryScriptException,
    EntryScriptInitException,
    EntryScriptInitTimeout,
    EntryScriptRunException,
    EntryScriptRunTimeout,
)
from telemetry_logger import log_error, log_warning
from progress_status import ProgressStatus
from job_progress_report import JobProgressReport
from poison_task import PoisonTask
from error_threshold import ErrorThreshold
from time_partition_logger import TimePartitionLogger


class ProgressSummary:
    """ Monitoring and reporting self.progress_store.
    """

    SUMMARY_UPDATE_INTERVAL_IN_SECOND = 1  # The interval to update processed summary.
    MAX_ERROR_COUNT = 3
    MAJOR_ERROR_RATE = 0.5  # Consider an error as the major cause if exceeding this rate

    def __init__(self, progress_store, total_tasks, total_items, error_threshold: ErrorThreshold):
        """
            :param progress_store, the store containing the processing result.
            :param total_tasks, created total tasks.
            :param total_items, created total items.
            :param error_threshold, the ErrorThreshold object.
        """
        self.logger = logger.get_logger()
        self.overview_logger = TimePartitionLogger()

        self.progress_store = progress_store
        self.total_tasks = total_tasks
        self.total_items = total_items

        self.succeeded_items = 0
        self.finished_tasks = 0

        if not isinstance(error_threshold, ErrorThreshold):
            raise ValueError(
                (
                    "The parameter 'error_threshold' must be an instance of ErrorThreshold."
                    f" The value you gave is {error_threshold}."
                )
            )

        self.error_threshold = error_threshold

    def summarize(self):
        """ Summarize the result of the job.
            Raise exception if 1) hitting error threshold or 2) processed_items is less than expected.
            This method should be called after all workers end and progress cache is updated.
        """

        processed_tasks, processed_items, succeeded_items, failed_items = self.progress_store.get_task_result_summary()

        self.finished_tasks = processed_tasks
        self.succeeded_items = succeeded_items

        JobProgressReport(self.progress_store).save()

        if self.total_items == 0:  # use processed items when total_items is not available.
            self.total_items = processed_items

        summary_message = (
            f"There are {self.total_tasks} {Constant.TERM_MINI_BATCHES} with {self.total_items} "
            f"{Constant.TERM_ITEMS}. "
            f"Processed {processed_tasks} {Constant.TERM_MINI_BATCHES} containing {processed_items} "
            f"{Constant.TERM_ITEMS}, {succeeded_items} succeeded, {failed_items} failed. The error "
            f"threshold is {self.error_threshold.allowed_failed_items}. "
        )

        self.logger.debug(summary_message)
        self.error_threshold.actual_failed_items = failed_items
        self.error_threshold.check()

        if processed_tasks == self.total_tasks:
            self.logger.info(Message.FINISHED_PROCESSED_ALL.format(summary_message))
        else:
            if processed_tasks > self.total_tasks:
                log_warning(Message.FINISHED_WARNING_PROCESSED_MORE_THAN_CREATED)
            else:  # processed_tasks < total_tasks
                self.logger.error(
                    f"The {Constant.TERM_PRODUCT_NAME} failed to process all {Constant.TERM_MINI_BATCHES}."
                )
                self.raise_exception()

    def check_entry_script_init_status(self):
        """ Check the init() error from workers."""
        count_by_status = self.progress_store.entry_script_init_status.count_by_status()
        self.logger.debug(f"entry_script_init_status.count_by_status:{count_by_status}")

        count_done = count_by_status[ProgressStatus.ENTRY_SCRIPT_INIT_DONE]

        excs = []
        count = count_by_status[ProgressStatus.ENTRY_SCRIPT_INIT_TIMEOUT]
        if count > 0:
            if count_done == 0 or count / count_done > 0.5:
                msg = (
                    f"The init() in the entry scipt had timeout for {count} times."
                    " Please increase --run_invocation_timeout and try again."
                    " Check logs/sys/perf to see if the node is overloaded."
                    " See logs/readme.txt for description of the log layout."
                )
                excs.append(EntryScriptInitTimeout(msg))

        count = count_by_status[ProgressStatus.ENTRY_SCRIPT_INIT_EXCEPTION]
        if count > 0:
            if count_done == 0 or count / count_done > 0.5:
                msg = (
                    f"The init() in the entry scipt had raised exception for {count} times."
                    " Please check workers log to find the cause."
                )
                excs.append(EntryScriptInitException(msg))

        if len(excs) == 1:
            raise excs[0]

        if len(excs) > 1:
            raise EntryScriptException(excs)

    def check_entry_script_run_status(self):
        """ Check the run() error from workers."""
        count_by_status = self.progress_store.entry_script_run_status.count_by_status()
        self.logger.debug(f"entry_script_run_status.count_by_status:{count_by_status}")

        count_done = len(self.progress_store.processed_tasks)

        self.logger.debug(f"entry_script_init_status.count_by_status:{count_by_status}, processed: {count_done}.")

        excs = []
        count = count_by_status[ProgressStatus.ENTRY_SCRIPT_RUN_TIMEOUT]
        if count > 0:
            if count_done == 0 or count / count_done > self.MAJOR_ERROR_RATE:
                msg = (
                    f"The run() in the entry scipt had timeout for {count} times."
                    " Please increase --run_invocation_timeout and try again."
                    " Check logs/sys/perf to see if the node is overloaded."
                    " See logs/readme.txt for description of the log layout."
                )
                excs.append(EntryScriptRunTimeout(msg))
        count = count_by_status[ProgressStatus.ENTRY_SCRIPT_RUN_EXCEPTION]
        if count > 0:
            if count_done == 0 or count / count_done > self.MAJOR_ERROR_RATE:
                msg = (
                    f"The run() in the entry scipt had raised exception for {count} times."
                    " Please check workers log to find the cause."
                )
                excs.append(EntryScriptRunException(msg))

        if len(excs) == 1:
            raise excs[0]

        if len(excs) > 1:
            raise EntryScriptException(excs)

    def raise_exception(self):
        """ Raise exception to end uers for failed case.
            Advise users how to move on in the messages.
        """

        try:
            if not self.progress_store.processed_tasks:  # no task processed
                if self.progress_store.pending_tasks:  # task picked, but not processed
                    poison_task = PoisonTask()
                    if poison_task.exists():  # some task are poisoned.
                        raise TaskPoisonedException(
                            len(self.progress_store.pending_tasks), len(self.progress_store.processed_tasks)
                        )

                    self.check_entry_script_init_status()
                    self.check_entry_script_run_status()
                    raise NoTaskProcessedException()

                # no task was picked
                self.check_entry_script_init_status()
                self.check_entry_script_run_status()
                raise NoTaskPickedException()

            # at lease one task processed, there must be pending tasks
            self.check_entry_script_init_status()
            self.check_entry_script_run_status()
            raise SomeTaskProcessedException(
                len(self.progress_store.pending_tasks), len(self.progress_store.processed_tasks)
            )
        except BaseException as exc:
            logger.get_user_error_logger().error(exc)
            self.overview_logger.flush(exc)
            log_error(f"Exception in progress summary: {exc}")
            raise exc
