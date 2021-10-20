# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides progress monitor features on master.
"""
import datetime
import time
import traceback
from threading import Thread

import utility
import logger
from constant import Constant, Message
from error_threshold import ErrorThreshold
from event import Event
from job_state import JobState
from telemetry_logger import log_error, log_warning, log_info
from metrics_logger import MetricsLogger
from progress_store import ProgressStore
from job_progress_report import JobProgressReport
from time_partition_logger import TimePartitionLogger


class ProgressMonitor:
    """ This class provides features to monitor progress.
    """

    SUMMARY_UPDATE_INTERVAL_IN_SECOND = 10  # The interval to update processed summary.
    MAX_ERROR_COUNT = 180  # 180 round consecutive failure, about 30 minutes in total.
    MAJOR_ERROR_RATE = 0.5  # Consider an error as the major cause if exceeding this rate

    def __init__(self, args):
        self.args = args
        self.start_time = utility.timestamp()
        self.logger = logger.get_logger()
        self.overview_logger = TimePartitionLogger()
        self.poll_count = 0  # The number of polling round.
        self.total_tasks = 0
        self.total_items = 0
        self.all_tasks_created = False
        self._all_tasks_processed = False
        self.processed_tasks = 0
        self.last_update_time = utility.timestamp()
        self.error_count = 0
        self.stopping = False
        self.threads = []
        self.error_threshold = ErrorThreshold(allowed_failed_items=self.args.error_threshold)
        self.progress_store = ProgressStore()
        self.before_stop = Event()  # This is for main process of master.
        self.job_state = JobState()  # This works for all nodes
        self.task_result_summary = None
        self.stop_reasons = []
        self.seconds_after_all_workers_stopped = 0
        self.metrics_logger = MetricsLogger(
            metrics_name_prefix=self.args.metrics_name_prefix, push_metrics_to_parent=self.args.push_metrics_to_parent
        )
        self.progress_updated = None
        self.job_progress_report = JobProgressReport(self.progress_store)

    def get_processed(self):
        """ Update processed cache.
            If the cache is updated, update processed tasks.
            The method always return False as it won't stop the poll.
        """
        self.task_result_summary = self.progress_store.get_task_result_summary()
        new_processed_tasks = self.task_result_summary[0]
        if new_processed_tasks > self.processed_tasks:
            self.metrics_logger.log_processing_status(new_processed_tasks, self.task_result_summary[1])
            # Log failed items if count is increased
            if (
                self.error_threshold.actual_failed_items < self.task_result_summary[3]
                and self.task_result_summary[3] > 0
            ):
                self.metrics_logger.log("Failed Items", self.task_result_summary[3])
            # Log remaining status only after all mini batches are created
            if self.total_items > 0:
                self.metrics_logger.log_remaining_status(
                    self.total_tasks - new_processed_tasks, self.total_items - self.task_result_summary[1]
                )

            self.progress_updated = True
            self.processed_tasks = new_processed_tasks
            self.last_update_time = utility.timestamp()
            self.error_threshold.actual_failed_items = self.task_result_summary[3]  # Notify error_threshold

            self.job_progress_report.save_processed()
        elif new_processed_tasks == self.processed_tasks:
            self.progress_updated = False
        else:
            message = f"processed task decreased from {self.processed_tasks} to {new_processed_tasks}. This should not happen."
            log_error(message)

        return False  # always continue to next action in the chain.

    def fmt_seconds(self, seconds):
        """Format seconds into readable text."""
        return str(datetime.timedelta(seconds=round(seconds)))

    def estimate_remaining_time(self):
        """Estimate remaining time."""
        elaspsed = utility.timestamp() - self.start_time
        if self.processed_tasks > 0:
            remaining_seconds = (self.total_tasks - self.processed_tasks) * elaspsed / self.processed_tasks
            message = (
                f"Processed {self.processed_tasks} of {self.total_tasks} {Constant.TERM_MINI_BATCHES}"
                f" in {self.fmt_seconds(elaspsed)}. Estimate remaining {self.fmt_seconds(remaining_seconds)}."
            )
            if remaining_seconds >= 300:  # Log one time in 12 rounds, i.e., about 2 minutes.
                if self.poll_count % 12 == 0:
                    self.overview_logger.flush(message)
            else:
                self.overview_logger.flush(message)
        else:
            self.overview_logger.flush("No task has been processed yet.")

    def all_tasks_processed(self):
        """ Return True to stop the poll if all tasks have been processed.
            Otherwise, check if all tasks have been processed if all tasks have been created.
        """
        if self._all_tasks_processed:
            return True

        if self.all_tasks_created:  # All task created
            if self.processed_tasks == self.total_tasks:
                message = Message.ALL_TASKS_RPOCESSED.format(self.total_tasks)
                self.overview_logger.flush(message)
                self._all_tasks_processed = True
                self.stop_reasons.append(message)
                return True

            if self.processed_tasks > self.total_tasks:
                message = Message.PROCESSED_MORE_THAN_CREATED.format(self.total_tasks, self.processed_tasks)
                self.stop_reasons.append(message)
                return True

            # Processed is less than scheduled
            self.estimate_remaining_time()
            return False

        # Task creation is in progress
        if self.processed_tasks > 0:
            message = f"Processed {self.processed_tasks} {Constant.TERM_MINI_BATCHES}."
            self.logger.debug(message)
            self.overview_logger.flush(message)

        return False  # continue to next action in the chain

    def timeout(self):
        """ Signal stop and return True if no progress update in the allowed duration.
            After a task created or processed, self.last_update_time will be updated to now.
        """
        wait_seconds = round(utility.timestamp() - self.last_update_time)

        if self.all_tasks_created:
            self.logger.debug(
                f"updated={self.progress_updated}, total wait from last update: {wait_seconds} seconds,"
                f" remaining {self.args.progress_update_timeout - wait_seconds} seconds."
                f" {self.processed_tasks}/{self.total_tasks} {Constant.TERM_ITEMS} processed."
            )
        else:
            self.logger.debug(
                f"updated={self.progress_updated}, total wait from last update: {wait_seconds} seconds,"
                f" remaining {self.args.progress_update_timeout - wait_seconds} seconds."
                f" {self.processed_tasks} {Constant.TERM_MINI_BATCHES} processed."
            )

        if wait_seconds >= self.args.progress_update_timeout:
            message = Message.STOP_REASON_PROGRESS_TIMEOUT.format(self.args.progress_update_timeout)
            log_error(message)
            self.stop_reasons.append(message)
            return True

        return False  # continue to next action in the chain

    def exceed_error_threshold(self):
        """ True if exceeding the threshold."""
        if self.error_threshold.exceeded():
            self.stop_reasons.append(Message.STOP_REASON_ERROR_THRESHOLD)
            return True

        return False

    def is_stopping(self):
        """ Return true if self.stopping is True."""
        if self.stopping:
            self.stop_reasons.append(Message.STOP_REASON_SET_STOPPING)

        return self.stopping

    def got_stop_signal(self):
        """" Return True if got stop signal."""
        if self.job_state.stopping():
            self.stop_reasons.append(Message.STOP_REASON_GOT_STOP_SIGNAL)
            return True

        return False

    def trigger_before_stop(self):
        """ Trigger the before_stop event."""
        try:
            self.logger.debug("Start to call all the event handlers of before_stop.")
            self.before_stop(self)
        except BaseException as exc:
            message = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format(
                "all the event handlers of before_stop", exc, traceback.format_exc()
            )
            self.logger.warning(message)

    def poll(self):
        """ Poll the progress by calling a list of methods and stop if any method returns True.
        """
        self.logger.debug(f"Start polling progress.")
        stop_conditions = [
            self.get_processed,
            self.all_tasks_processed,
            self.timeout,
            self.is_stopping,
            self.got_stop_signal,
            self.exceed_error_threshold,
        ]

        self.metrics_logger.log("Failed Items", 0)
        self.metrics_logger.log_processing_status(0, 0)

        count = 0
        while True:
            try:
                count += 1
                self.poll_count = count
                stop = False
                for condition in stop_conditions:
                    if condition():
                        stop = True
                        break

                if stop:
                    break

                time.sleep(self.SUMMARY_UPDATE_INTERVAL_IN_SECOND)  # sleep and then try

                if count % 100 == 1:
                    self.logger.info(f"Polled {count} times.")

                self.error_count = 0  # Reset to zero if this round succeeds.
            except BaseException as exc:
                message = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format(
                    f"poll progress on round {count}", exc, traceback.format_exc()
                )
                self.logger.warning(message)
                self.error_count += 1
                if self.error_count > self.MAX_ERROR_COUNT:
                    log_error(Message.EXCEEDED_MAX_ERROR_COUNT.format(count))
                    break

        message = f"Progress update stopped for reasons: {self.stop_reasons}."
        log_info(message)
        self.overview_logger.flush(message)

        self.trigger_before_stop()

        log_info(f"Finished polling progress.")

    def start(self):
        """ start thread to update summary.
            Use thread as this needs to check states in the main processes.
            Consider a thread won't hang here as it doesn't call user code.
        """
        thr = Thread(target=self.poll, args=())
        thr.start()
        self.threads.append(thr)

        log_info(f"poll() thread started.")

    def wait(self):
        """ Wait the poll thread to finish."""
        self.logger.info("Start waiting for the update summary thread to end.")
        for thr in self.threads:
            try:
                thr.join()
            except BaseException as exc:  # pylint: disable=broad-except
                # Sallow so that the master can report based on processing result.
                message = Message.FAILED_TO_JOIN_THREAD.format(exc, traceback.format_exc())
                self.logger.error(message)

        log_info("All threads finished.")

    def signal_stop(self):
        """ Notify to stop and poll() will stop on next polling.
        """
        log_info("Got stop signal.")
        self.stopping = True
