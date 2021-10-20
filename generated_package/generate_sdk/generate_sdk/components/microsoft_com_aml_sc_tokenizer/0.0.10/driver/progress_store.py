# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides a store to track progress.
"""
import os
from multiprocessing import current_process

from constant import Constant
from progress_status import ProgressStatus
from progress_record import ProgressRecord
from entry_script_init_store import EntryScriptInitStore
from entry_script_run_store import EntryScriptRunStore
from utility import get_ip
import logger
from log_config import LogConfig
from task_result import TaskResult
from azure_queue_helper import AzureQueueHelper
from run_context_factory import RunContextFactory
from worker_progress_report import WorkerProgressReport


class ProgressStore:
    """ A progress store in memory to track progress.
        Workers enque picked and finished tasks to processed queue.
        The master deques above messages to calculate progress.
    """

    MAX_PROGRESS_MESSAGE_COUNT_TO_READ = 10

    def __init__(self):
        self.logger = logger.get_logger()
        self.run_context = RunContextFactory.get_context()
        self.queue_helper = AzureQueueHelper(Constant.PROCESSED_TASK_QUEUE_PREFIX + self.run_context.run_id)
        self.processed_tasks = dict()  # run() returned, including succeeded items and failed items.
        self.poisoned_tasks = dict()  # poisoned tasks, messages being picked on the fourth time.
        self.pending_tasks = dict()  # The value is a list of task result
        self.entry_script_init_status = EntryScriptInitStore()  # Track entry script init()
        self.entry_script_run_status = EntryScriptRunStore()

        # Tasks override by later one.
        # This happens if a task being processed more than once. The value is a list of task result
        self.override_tasks = dict()

        ip_address = get_ip()
        self.dir = os.path.join(LogConfig().log_dir, "sys/worker", ip_address)
        os.makedirs(self.dir, exist_ok=True)

        # total processed tasks + poisoned tasks, processed items, succeeded items, failed items
        self.summary = (0, 0, 0, 0)

        os.makedirs(self.dir, exist_ok=True)

        self.worker_progress_report = WorkerProgressReport()

    def __reduce__(self):
        return (self.__class__, ())

    def add_override(self, prior):
        """ Add to override_tasks
        """
        assert prior.status == ProgressStatus.TASK_PROCESSED, "The status must be TASK_PROCESSED."

        task_id = prior.id
        if task_id in self.override_tasks:
            self.override_tasks[task_id].append(prior)
        else:
            self.override_tasks[task_id] = [prior]

    def remove_pending(self, task_result):
        """ As queue message may not come in sequence, a finished task may not have a matched pending one.
        """
        if task_result.id in self.pending_tasks:
            task_list = self.pending_tasks[task_result.id]

            for task in task_list:
                if task_result.match(task):
                    task_list.remove(task)
                    if not task_list:
                        del self.pending_tasks[task_result.id]
                    break

    def update_result(self, task_result):
        """ For a pending task, add it pending_tasks.
            For a processed task:
                1) If there is prior one with same task id, move prior to override_tasks.
                2) Add this one to processed_tasks.
                3) Remove the one in pending tasks
            TODO: This assumes task result will be deque in order.
                Mesages may not be dequed strictly as first-in-first-out.
                That means the 'later' one may not be late actually.
                Using the timestamp in task result also has problem, as it need all the clocks on nodes
        """
        status = task_result.status
        assert status in [
            ProgressStatus.TASK_PICKED,
            ProgressStatus.TASK_PROCESSED,
            ProgressStatus.TASK_POISONED,
        ], "The status must be in the supported ones."
        task_id = task_result.id
        if task_result.status == ProgressStatus.TASK_PICKED:
            if task_id in self.pending_tasks:
                self.pending_tasks[task_id].append(task_result)
            else:
                self.pending_tasks[task_id] = [task_result]

        elif task_result.status == ProgressStatus.TASK_PROCESSED:
            self.remove_pending(task_result)
            if task_id not in self.processed_tasks:
                self.processed_tasks[task_result.id] = task_result
                self.summary = (
                    len(set(self.processed_tasks.keys()).union(set(self.poisoned_tasks.keys()))),
                    self.summary[1] + task_result.total,
                    self.summary[2] + task_result.succeeded,
                    self.summary[3] + task_result.failed,
                )
            else:
                # If a message in azure storage queue is picked up by more than once,
                #  there will be duplicate task results.
                # Override the prior one and save the prior to duplicate.txt for troubleshooting.
                # Use should override prior result with the current result to ensure consistency.
                # TODO: should we keep the better result here? e.g., the prior one may have more succeeded items.
                prior = self.processed_tasks[task_result.id]
                prior.by = task_result
                self.add_override(prior)

                self.processed_tasks[task_result.id] = task_result
                self.summary = (
                    len(set(self.processed_tasks.keys()).union(set(self.poisoned_tasks.keys()))),
                    self.summary[1] + task_result.total - prior.total,
                    self.summary[2] + task_result.succeeded - prior.succeeded,
                    self.summary[3] + task_result.failed - prior.failed,
                )
        elif task_result.status == ProgressStatus.TASK_POISONED:
            self.poisoned_tasks[task_id] = task_result  # one message will at most be poisoned one time.
            if task_id not in self.processed_tasks:  # consider the task as failed for all items.
                self.poisoned_tasks[task_id] = task_result
                self.summary = (
                    len(set(self.processed_tasks.keys()).union(set(self.poisoned_tasks.keys()))),
                    self.summary[1] + task_result.total,
                    self.summary[2] + task_result.succeeded,
                    self.summary[3] + task_result.failed,
                )

    def dispatch(self, message):
        """ Dispatch the message to the corresponding table according its type."""
        record = ProgressRecord.from_json(message.content)
        status = record.status  # pylint: disable=no-member
        # TODO: Change TaskResult to inherit from ProgressRecord or remove TaskResult
        if status in [ProgressStatus.TASK_PICKED, ProgressStatus.TASK_PROCESSED, ProgressStatus.TASK_POISONED]:
            task_result = TaskResult.from_json(message.content)
            self.update_result(task_result)
        elif status in [
            ProgressStatus.ENTRY_SCRIPT_INIT_DONE,
            ProgressStatus.ENTRY_SCRIPT_INIT_EXCEPTION,
            ProgressStatus.ENTRY_SCRIPT_INIT_START,
            ProgressStatus.ENTRY_SCRIPT_INIT_TIMEOUT,
        ]:
            self.entry_script_init_status.add(record)
        elif status in [
            ProgressStatus.ENTRY_SCRIPT_RUN_DONE,
            ProgressStatus.ENTRY_SCRIPT_RUN_EXCEPTION,
            ProgressStatus.ENTRY_SCRIPT_RUN_START,
            ProgressStatus.ENTRY_SCRIPT_RUN_TIMEOUT,
        ]:
            self.entry_script_run_status.add(record)
        else:
            raise ValueError(f"While processing messages from queue, received unknown status: {status}")

    def get_task_results(self):
        """ This method picks up task results from azure storage queue, append to existing results.
            And then returns the list of processed task results.

            As this method consumes the message in azure queue, it has side effects.
            It can only be called in one instance to return correct result.
        """
        messages = self.queue_helper.get_messages(num_messages=self.MAX_PROGRESS_MESSAGE_COUNT_TO_READ)
        while messages:
            for message in messages:
                self.dispatch(message)
                self.queue_helper.delete_message(message)
                self.logger.debug(f"Got a message from worker: {message.content}.")
            messages = self.queue_helper.get_messages(num_messages=self.MAX_PROGRESS_MESSAGE_COUNT_TO_READ)

        return self.processed_tasks

    def get_task_result_summary(self):
        """ Return a tuple including the number of total, succeeded and failed processed items

            As this method consumes the message in azure queue, it has side effects.
            It can only be called in one instance to return correct result.
        """
        self.get_task_results()  # Poll result from queue if there is any

        return self.summary

    def notify_progress(self, task_result):
        """ Report processed item to processed item queue.
            Called in worker process.
        """
        self.queue_helper.put_message(task_result.to_json())  # notify the master
        self.save_progress(task_result)

    def save_progress(self, task_result):
        """ Append to the processed task to the progress file.
        To avoid racing condition, one process on one worker will have a progress file.
        """
        self.worker_progress_report.save_progress(task_result)

    def processed(self, task_result):
        """ Return True if the pending task has been already processed."""
        if task_result.id in self.processed_tasks:
            if self.processed_tasks[task_result.id].match(task_result):
                return True

        if task_result.id in self.override_tasks:
            for task in self.override_tasks[task_result.id]:
                if task.match(task_result):
                    return True

        return False

    def remove_processed(self):
        """ Check if a pending task is finished again as the queue message may not deque in order.
        """
        task_id_to_delete = []
        for task_id in self.pending_tasks:
            to_delete = []
            task_list = self.pending_tasks[task_id]
            for task in task_list:
                if self.processed(task):
                    to_delete.append(task)
            for task in to_delete:
                task_list.remove(task)

            if not task_list:
                task_id_to_delete.append(task_id)

        # Remove key from dict whose value is an empty list
        for task_id in task_id_to_delete:
            del self.pending_tasks[task_id]
