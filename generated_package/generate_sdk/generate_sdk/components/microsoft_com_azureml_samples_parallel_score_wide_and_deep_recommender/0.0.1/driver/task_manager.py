# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides task management related features on an azure storage queue helper.
"""
from concurrent import futures
import time
import traceback

import utility
from exception import TaskCreationException
from azure_queue_helper import AzureQueueHelper
from constant import Constant, Message
from event import Event
from job_state import JobState
from telemetry_logger import log_error, log_warning, log_task_manager_telemetry
import logger
from logger import get_logger
from metrics_logger import MetricsLogger
from task import TaskToQueue, TaskInAzureQueue
from poison_task import PoisonTask
from run_context_factory import RunContextFactory
from time_partition_logger import TimePartitionLogger


class TaskManager:
    """This class manages tasks on an azure storage queue helper."""

    MAX_RETRY_TIMES = 2
    MAX_DEQUEUE_COUNT = 3
    MAX_WORKERS_IN_TASK_CREATION = 10  # The max threads for task creation in thread pool.
    POLLING_MESSAGE_INTERVAL = (
        1  # The time to sleep before trying to get next message from queue if no message returned.
    )
    BASE_RETRY_INTERVAL = 1

    def __init__(self, args):

        self.logger = get_logger()
        self.args = args
        self.run_context = RunContextFactory.get_context()

        # log warnings if exceeding this value
        self.long_wait = 2 * self.args.run_invocation_timeout
        name_postfix = AzureQueueHelper.name_from_run_id(self.run_context.run_id)
        self.azure_queue = AzureQueueHelper(Constant.PENDING_TASK_QUEUE_PREFIX + name_postfix)
        self.overview_logger = TimePartitionLogger()
        self.job_state = JobState()
        self.poison_task = PoisonTask()
        self.metrics_logger = MetricsLogger(
            metrics_name_prefix=self.args.metrics_name_prefix, push_metrics_to_parent=self.args.push_metrics_to_parent
        )

        self.provider_init_duration = None
        self.first_task_duration = None
        self.total_scheduling_time = None
        self.stop_task_creation = False  # If true, stop task creation
        self.start_time_perf_counter = time.perf_counter()

        self.total_to_create, self.total_created = 0, 0
        self.total_created_roughly = 0  # counting not in a thread-safe way, use for logging only
        self.exceptions = []
        self.failed_tasks = []

        # Trigger when a task created.
        # With parameters:
        # (sender, task_id)
        self.on_task_created = Event()

    def retry(self, function, *args):
        """ Retry to run a function if failed."""
        max_retry_times = self.MAX_RETRY_TIMES

        exceptions = []
        traces = []
        for i in range(1, max_retry_times + 2):
            try:
                return function(*args)  # exit if no error.
            except BaseException as exc:
                exceptions.append(exc)
                trace = traceback.format_exc()
                traces.append(trace)
                if i >= max_retry_times + 1:
                    message = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format(
                        f"retry on round {i} over {max_retry_times}", exc, trace
                    )
                    self.logger.error(message)
                    raise Exception(exceptions, ",".join(traces))

                sleep_seconds = 2 ** i
                message = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format(
                    f"retry on round {i} over {max_retry_times}. Will retry after sleep {sleep_seconds} seconds.",
                    exc,
                    trace,
                )
                self.logger.warning(message)
                time.sleep(sleep_seconds * self.BASE_RETRY_INTERVAL)

    def add_task(self, task):
        """Add a task to task list."""
        task_in_json = task.to_json()
        self.azure_queue.put_message(task_in_json)

    def save_and_delete_poison_tasks(self, messages):
        """ Save the poison messages to file and delete them from azure storage queue."""
        if messages:
            for message in messages:
                self.poison_task.add(message)
                self.azure_queue.delete_message(message)

    def get_tasks(self, visibility_timeout):
        """ Fetch message from the azure storage queue and return as an instance of TaskInAzureQueue
            If no message returned from the queue, sleep and then fetch again until got stop signal.
            Return empty list if got stop signal.
            :visibility_timeout, the invisible time of the returned task.
             The invisibility can be extended with update_task
            :return: A list of zero, one, or more tasks.
            :rtype: list of :class:`TaskInAzureQueue`.
        """
        start_time = utility.timestamp()
        while True:
            if self.stop_task_creation or self.job_state.stopping():
                self.logger.info(
                    Message.GOT_STOP_SIGNAL.format("Return empty task list and the worker process will end soon.")
                )
                return []
            messages = self.azure_queue.get_messages(visibility_timeout=visibility_timeout)
            if messages:
                poison_tasks = []
                valid_messages = []
                for message in messages:
                    if message.dequeue_count > self.MAX_DEQUEUE_COUNT:
                        self.logger.debug(f"Found poison message {message.content}.")
                        poison_tasks.append(message)
                    else:
                        valid_messages.append(message)

                self.save_and_delete_poison_tasks(poison_tasks)

                if valid_messages:
                    return [TaskInAzureQueue(message) for message in messages]

            else:
                wait_seconds = round(utility.timestamp() - start_time)
                if logger.keep(wait_seconds):
                    if wait_seconds <= self.long_wait:
                        self.logger.debug(f"Total waiting time: {wait_seconds} second.")
                    else:
                        message = Message.LONG_WAIT_IN_GET_TASKS.format(wait_seconds)
                        log_warning(message)

            time.sleep(self.POLLING_MESSAGE_INTERVAL)

    def delete_task(self, task: TaskInAzureQueue):
        """ Delete the task from Azure Storage Queue."""
        self.azure_queue.delete_message(task.message)

    def create_task(self, task: TaskToQueue):
        """ Create a task."""
        self.add_task(task)
        self.on_task_created(self, task.id)
        if self.first_task_duration is None:
            self.first_task_duration = time.perf_counter() - self.start_time_perf_counter

    def create_task_with_retry(self, task: TaskToQueue):
        """ Retry to create a task if failed.
            Return task id if created sucessfully. Only return task id to reduce memory usage.
            Return None if received stop signal.
        """
        try:
            self.retry(self.create_task, task)

            if logger.keep(task.id):
                self.logger.info(f'Sent "{task.to_json()}" to queue.')

            self.total_created_roughly += 1
            if logger.keep(self.total_created_roughly):
                elapsed = time.perf_counter() - self.start_time_perf_counter
                message = (
                    f"Scheduled {self.total_created_roughly} {Constant.TERM_MINI_BATCHES}"
                    f" in {round(elapsed)} seconds."
                )
                self.logger.info(message)
                self.overview_logger.put(message)

            return task.id
        except BaseException as exc:
            self.failed_tasks.append(task)
            self.exceptions.append(exc)

            # stop the loop to submit to thread pool if not finishes.
            self.stop_task_creation = True
            message = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format(
                f"create task {task.to_json()}.", exc, traceback.format_exc()
            )
            log_error(message)
            raise exc

    def create_tasks(self, task_provider):
        """ Create tasks."""
        message = "Start scheduling."
        self.logger.debug(message)
        self.overview_logger.put(message)

        with futures.ThreadPoolExecutor(max_workers=self.MAX_WORKERS_IN_TASK_CREATION) as executor:
            future_tasks = []
            for task in task_provider.get_tasks():
                self.total_to_create += 1
                if self.stop_task_creation or self.job_state.stopping():
                    message = Message.GOT_STOP_SIGNAL.format(
                        f"Scheduling stopped on creating {self.total_to_create} {Constant.TERM_MINI_BATCHES}."
                    )
                    self.overview_logger.put(message)
                    self.logger.warning(message)
                    self.job_state.exit(message)  # raise SystemExit with 82 to break the loop

                future = executor.submit(self.create_task_with_retry, task)
                future_tasks.append(future)

            for future in futures.as_completed(future_tasks):
                exception = future.exception()

                if exception is None:
                    self.total_created += 1

                else:
                    self.exceptions.append(exception)
                    message = Message.FAILED_ACTION_WITH_ERROR.format(f"create tasks", exception)
                    self.logger.error(message)
                    self.overview_logger.put(message)

        if self.failed_tasks or self.exceptions:
            raise TaskCreationException(self.failed_tasks, self.exceptions)

        total_items = task_provider.total_items
        queue_time = round(time.perf_counter() - self.start_time_perf_counter)

        self.metrics_logger.log("Total MiniBatches", self.total_created)
        total_items_message = ""
        if total_items > 0:
            self.metrics_logger.log("Total Items", total_items)
            self.logger.info(f"TaskManager - Total number of {Constant.TERM_ITEMS}: {total_items}.")
            total_items_message = f" with {total_items} {Constant.TERM_ITEMS}"

        message = (
            f"Scheduling finished. Scheduled {self.total_created} {Constant.TERM_MINI_BATCHES}"
            f"{total_items_message} in {queue_time} seconds."
        )
        self.logger.debug(message)
        self.overview_logger.put(message)

        self.provider_init_duration = task_provider.init_duration
        self.total_scheduling_time = queue_time

        log_task_manager_telemetry(
            self.total_to_create, total_items, task_provider.init_duration, self.first_task_duration, queue_time
        )

    def force_stop_task_creation(self):
        """ Force to stop task creation"""
        self.stop_task_creation = True

    def renew_task_lease(self, task: TaskInAzureQueue, lease: int):
        """ Renew the lease of the task in Azure Storage Queue.
            lease: new lease in second.
        """
        self.azure_queue.update_message_visibility_timeout(task.message, lease)
