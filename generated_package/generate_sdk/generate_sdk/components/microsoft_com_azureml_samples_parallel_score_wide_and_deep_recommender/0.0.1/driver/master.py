# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides master implementation to create tasks and manages workers.
"""
import os
from pathlib import Path
from multiprocessing import current_process
import time
import traceback

import utility
from log_config import LogConfig
from exception import (
    FirstTaskCreationTimeout,
    EntryScriptException,
    DriverException,
    UserInputNotFoundError,
    NoResultToAppendError,
)
from azure_queue_helper import AzureQueueHelper
from constant import Constant, Message
from job_state import JobState
from telemetry_logger import log_info, log_warning, log_job_start_telemetry
from node import Node
from process_helper import ProcessHelper
from progress_monitor import ProgressMonitor
from progress_summary import ProgressSummary
from queue_cleaner import QueueCleaner
from task_producer import TaskProducer
from file_helper import FileHelper


class Master(Node):
    """ The class for ParallelRunStep master node.

    A *master* represents the master node inside of an AmlCompute Batch Inferencing cluster.

    .. remarks::

        A *master* represents the master node inside of an AmlCompute Batch Inferencing cluster.
        A master is the object used to provide the shared features of Master node.

        Functionality includes:

        *  Create an azure storage queue.
        *  Create tasks synchronously or asynchronously.
        *  Wait for workers to finish processing all tasks and delete the queue.
        *  Monitoring and reporting progress.
        *  Concat temp files for append_row.

        TODO: the master can know if the number of total, running workers, if workers post heartbeat back.
            the master can also tell which worker is alive based on the picked/processed messages.

            If the master sent stop signal, should it wait for all workers to end?
            There is not a reliable way to ensure all workers to post back their end signal.
    """

    POLLING_INTERVAL = 1  # interval to check if the first task created

    def __init__(self, args):
        super().__init__(args)
        assert current_process().name == "MainProcess"  # Ensure this class only runs in main process

        # Increase the niceness, i.e., lower the priority, of the current process.
        # This will change the main process and all new processes.
        # The goal is to yield more resources to AmlCompute processes.
        ProcessHelper().nice(nice=self.args.nice)

        run_id = self.run_context.run_id
        name_postfix = AzureQueueHelper.name_from_run_id(run_id)
        self.queue_names = [
            Constant.PENDING_TASK_QUEUE_PREFIX + name_postfix,
            Constant.PROCESSED_TASK_QUEUE_PREFIX + name_postfix,
        ]

        log_info(f"The queues are {self.queue_names}.")

        # Delete the queues so that the job can run with same run id as previous ones.
        self.clear_messages_in_queues()
        self.create_queues()

        if self.args.output:
            os.makedirs(self.args.output, exist_ok=True)

        self.job_state = JobState()
        self.task_producer = TaskProducer(self.args)
        self.task_producer.on_task_created += self.on_task_created
        self.task_producer.on_all_tasks_created += self.on_all_tasks_created
        self.first_task_created = False
        self.progress_monitor = ProgressMonitor(self.args)
        self.progress_monitor.before_stop += self.progress_monitor_before_stop
        self.concat_file_time = None
        self.concat_file_count = 0
        self.queue_cleaner = None
        if self.args.cleanup_leaked_queues:
            self.queue_cleaner = QueueCleaner()

        self.logger.info("Master - Starting")

    def create_queues(self):
        """ Create all job queues.
        """
        for name in self.queue_names:
            AzureQueueHelper(name).create_queue()

    def delete_queues(self):
        """ Delete Pending and Processed queues.
            Swallow exceptions if failed as:
                1) We don't want to fail the job.
                2) The next run will try to cleanup leaked queues again.
        """
        for name in self.queue_names[0:2]:
            try:
                AzureQueueHelper(name).delete_queue()
            except BaseException as exc:
                self.logger.warning(f"Failed to delete queue {name} with error {exc}.")

    def wait_for_input_init(self):
        """ Poll and return if the first task is created.
            Raise FirstTaskCreationTimeout if exceeding the time limit.
            This method runs in the main thread and will fail the job when it raises an exception.

            For dataprep api, it may take 10+ seconds to several minutes in the worst case to initialize.
        """
        start_time = utility.timestamp()
        count = 0
        while not self.first_task_created:
            count += 1
            wait_seconds = round(utility.timestamp() - start_time)
            if wait_seconds > self.args.first_task_creation_timeout:
                self.task_producer.force_stop_task_creation()
                exc = FirstTaskCreationTimeout(self.args.first_task_creation_timeout)
                log_warning(str(exc))
                raise exc

            if count % 60 == 0:  # warning around every 60 seconds
                self.logger.warning(Message.LONG_WAIT_FOR_FIRST_TASK_CREATION.format(wait_seconds))

            time.sleep(self.POLLING_INTERVAL)

    def clear_messages_in_queues(self):
        """Clear messages from the existing queues."""
        for name in self.queue_names:
            helper = AzureQueueHelper(name)
            if helper.exists():
                helper.clear_messages()

    def get_versions(self):
        """Return azureml-core and azureml-dataprep."""
        from pkg_resources import get_distribution

        core_version = ""
        dataprep_version = ""
        try:
            core_version = get_distribution("azureml-core").version
        except Exception:  # pylint: disable=broad-except
            from azureml.core import VERSION as core_version

        try:
            dataprep_version = get_distribution("azureml-dataprep").version
        except Exception:  # pylint: disable=broad-except
            try:
                from azureml.dataprep import __version__ as dataprep_version
            except Exception:  # pylint: disable=broad-except
                self.logger.exception("Unable to get dataprep version")

        return (core_version, dataprep_version)

    def _start(self):
        """Start a process to create tasks and update completed summary."""
        log_info(
            "Master - Start processing batch: "
            f"outputAction:{self.args.output_action}, miniBatchSize:{self.args.mini_batch_size}, "
            f"processCountPerNode:{self.args.process_count_per_node}, errorThreshold:{self.args.error_threshold}, "
            f"numberOfNodes:{os.environ.get('AZUREML_NODE_COUNT')}"
        )
        if self.args.using_tabular_dataset:
            input_format = "Tabular"
        else:
            input_format = "File"

        (core_version, dataprep_version) = self.get_versions()
        log_job_start_telemetry(
            input_format=input_format,
            output_action=self.args.output_action,
            mini_batch_size=self.args.mini_batch_size,
            process_count_per_node=self.args.process_count_per_node,
            error_threshold=self.args.error_threshold,
            client_sdk_version=self.args.client_sdk_version,
            aml_core_version=core_version,
            dataprep_version=dataprep_version,
            number_of_nodes=os.environ.get("AZUREML_NODE_COUNT"),
        )
        self.logger.info("Job telemetry sent.")

        self.task_producer.start()  # Start thread to create tasks
        self.logger.info("wait_for_input_init returned.")
        self.wait_for_input_init()

        if self.queue_cleaner:
            self.queue_cleaner.start()
            self.logger.info("queue_cleaner started.")

        self.progress_monitor.start()
        self.logger.info("Master - Started task producer and progress monitor")

    def get_profile_filename(self):
        """Return the filename for profile output."""
        log_dir = LogConfig().log_dir
        profile_dir = Path(log_dir) / "sys"
        profile_dir.mkdir(parents=True, exist_ok=True)
        return str(profile_dir / "master.profile")

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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ Delete the queues on exit."""
        self.delete_queues()

    def check_task_producer_result(self):
        """ Check if task producer has errors.
            If there is any error, signal to stop all threads, workers
            and raise exception to report the result to end users.

            The method must be called in main process, so that the exception can be raised to users.
        """
        if self.task_producer.exceptions:
            self.progress_monitor.signal_stop()
            self.progress_monitor.wait()
            self.job_state.signal_stop(f"Scheduling {Constant.TERM_MINI_BATCHES} failed.")
            if len(self.task_producer.exceptions) == 1:
                raise self.task_producer.exceptions[0]

            raise Exception(self.task_producer.exceptions)

    def summarize(self):
        """ Summarize the result.
            If failed, raise error to users.
         """
        pgr = self.progress_monitor
        summary = ProgressSummary(
            progress_store=pgr.progress_store,
            total_tasks=pgr.total_tasks,
            total_items=pgr.total_items,
            error_threshold=pgr.error_threshold,
        )
        summary.summarize()
        if self.args.output_action == "append_row" and summary.succeeded_items == 0:
            if summary.finished_tasks > 0:
                msg = (
                    "run() was unable to successfully process any mini batches."
                    " Please check 'response: run()' in https://aka.ms/batch-inference-documentation"
                )
            else:
                msg = f"All {summary.total_tasks} mini batches failed. There is no result returned."
            raise NoResultToAppendError(msg)

    def wait(self):
        """Wait until all threads/processes end."""
        self.logger.info("Master - Waiting for all workers to finish...")

        self.task_producer.wait()
        self.check_task_producer_result()

        if self.queue_cleaner:
            self.queue_cleaner.wait()

        self.progress_monitor.wait()  # Stop signal to workers sent before progress monitor ends
        try:
            self.summarize()
        except (EntryScriptException, DriverException, UserInputNotFoundError) as exc:
            self.logger.info(f"{exc}")
            # Don't save these exceptions as they are saved in progress monitor.
            raise

        except BaseException as exc:  # pylint: disable=broad-except
            # Failed for system error, not user error.
            detail = f"The master role failed with error {exc}. Detail: {traceback.format_exc()}."
            log_info(detail)
            raise

        if self.args.output_action == "append_row":
            log_info("Start concatenating.")
            start = utility.timestamp()
            file_helper = FileHelper(self.args)
            file_helper.start()
            self.concat_file_time = utility.timestamp() - start
            self.concat_file_count = file_helper.file_count

        log_info("Master - All workers finished")

    def on_task_created(self, sender, task_id):  # pylint: disable=unused-argument
        """ Event handler for a task created.
            This is not thread-safe as task creation runs in multiple threads.
            It's possible to set first_task_created more than one time.
            Using poll to avoid lock.
        """
        if not self.first_task_created:
            self.first_task_created = True

        self.progress_monitor.last_update_time = utility.timestamp()

    def on_all_tasks_created(self, sender):
        """ Event handler for all tasks created.
        """
        self.logger.debug(
            f"Finished to schedule all {sender.total_tasks} {Constant.TERM_MINI_BATCHES}. Notify the progress monitor."
        )
        self.progress_monitor.all_tasks_created = True
        self.progress_monitor.total_tasks = sender.total_tasks
        self.progress_monitor.total_items = sender.total_items

    def progress_monitor_before_stop(self, sender):  # pylint: disable=unused-argument
        """ Event handler for the progress_monitor.before_stop event.
        """
        # Notify all nodes to stop.
        self.job_state.signal_stop("Progress monitor is stopping.")
