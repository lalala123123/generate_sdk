# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides job related features.

Note: this module will be removed after moving to masterless mode.
    as in masterless mode, the entry point will start master as well as worker.
"""
import os
import sys
import time
import traceback
from datetime import datetime

from telemetry_logger import log_job_end_telemetry, log_error, log_info
import logger
import utility
from log_config import LogConfig
from master import Master
from worker_manager import WorkerManager
from entry_script_exception import EntryScriptException
from exception import UserException, NoResultToAppendError, UserInputNotFoundError
from standard_fields import AzureMLTelemetryTaskResult
from run_context_factory import RunContextFactory


class Job:
    """The class for ParallelRunStep execution.

    A *job* represents one execution of a ParallelRunStep.

    .. remarks::

        A *job* represents one execution of a ParallelRunStep.
        A job is the object used to provide the shared features of jobs.

        Functionality includes:

        *  Start job on single node.
        *  Start job on multiple node cluster.
    """

    def __init__(self, args):
        self.args = args
        log_config = LogConfig()
        log_config.config(self.args.logging_level)  # Setup top level log
        # log_config.config_overview()
        self.logger = logger.get_logger()

    def get_status(self):
        """Return the run status."""
        run = RunContextFactory.get_context().run
        return run.get_status()

    def run_canceled(self):
        """Return True if the run was canceled."""
        status = self.get_status()
        log_info(f"Run status: {status}")
        return status in ["Canceled", "CancelRequested"]

    def start(self):  # pylint: disable=too-many-locals
        """ Start a job and wait it to finish."""
        log_info(f"Job - Starting, master node: {os.environ.get('AZ_BATCH_MASTER_NODE')}")
        start_time = utility.timestamp()
        start_time_perf_counter = time.perf_counter()
        start_time_process_time = time.process_time()

        (completed_tasks, completed_items, succeeded_items, failed_items) = (0, 0, 0, 0)
        job_result = int(AzureMLTelemetryTaskResult.Success)
        failure_reason = None
        exception_type = None
        output_action = self.args.output_action
        mini_batch_size = self.args.mini_batch_size
        process_count_per_node = self.args.process_count_per_node
        error_threshold = self.args.error_threshold
        provider_init_duration = None
        first_task_creation = None
        total_scheduling_time = None
        concat_file_time = None
        concat_file_count = 0
        number_of_nodes = os.environ.get("AZUREML_NODE_COUNT", 1)

        if self.args.using_tabular_dataset:
            input_format = "Tabular"
        else:
            input_format = "File"

        try:
            is_current_node_master = os.environ.get("AZ_BATCH_IS_CURRENT_NODE_MASTER")
            if is_current_node_master is not None and is_current_node_master.lower() != "true":
                raise ValueError(
                    "A job can only run on the master node in single or multi-node AmlCompute cluster "
                    'The environment variable "AZ_BATCH_IS_CURRENT_NODE_MASTER" must be None or "true" on this node. '
                    f'The actual value is "{is_current_node_master}"'
                )

            with Master(self.args) as master:
                master.start()
                worker_manager = WorkerManager()
                worker_manager.start()
                worker_manager.wait()

                master.wait()
                provider_init_duration = master.task_producer.task_manager.provider_init_duration
                first_task_creation = master.task_producer.task_manager.first_task_duration
                total_scheduling_time = master.task_producer.task_manager.total_scheduling_time
                concat_file_time = master.concat_file_time
                concat_file_count = master.concat_file_count

                log_info("Job - Ending")

                (
                    completed_tasks,
                    completed_items,
                    succeeded_items,
                    failed_items,
                ) = master.progress_monitor.progress_store.get_task_result_summary()
        except (EntryScriptException, UserException, NoResultToAppendError, UserInputNotFoundError) as exc:
            # Don't write trace as this is known exception.
            log_error(f"UserException occurred executing job: {exc}")
            self.logger.error(f"UserException occurred executing job: {exc}.\n{traceback.format_exc()}")
            failure_reason = "UserError"
            raise
        except BaseException as exc:
            log_error(f"Exception occurred executing job: {exc}.\n{traceback.format_exc()}")

            if self.run_canceled():
                failure_reason = "UserError"
                msg = "User cancelled the run."
                log_info(msg)
                raise Exception(msg)

            failure_reason = "SystemError"
            raise
        finally:
            log_info(f"The run's status is {self.get_status()}.")
            if self.args.using_tabular_dataset:
                input_ds_count = len(self.args.input_tabular_datasets)
            else:
                input_ds_count = len(self.args.inputs)
            if failure_reason:
                job_result = int(AzureMLTelemetryTaskResult.Failure)
                exception_type = Job._get_exception_type()
            log_job_end_telemetry(
                start_time=start_time,
                end_time=utility.timestamp(),
                duration=utility.timestamp() - start_time,
                input_format=input_format,
                input_ds_count=input_ds_count,
                output_action=output_action,
                mini_batch_size=mini_batch_size,
                process_count_per_node=process_count_per_node,
                error_threshold=error_threshold,
                number_of_nodes=number_of_nodes,
                first_task_creation_time=first_task_creation,
                total_scheduling_time=total_scheduling_time,
                total_tasks=succeeded_items + failed_items,
                total_items=succeeded_items + failed_items,
                processed_tasks=completed_tasks,
                processed_items=completed_items,
                failed_items=failed_items,
                concat_file_time=concat_file_time,
                concat_file_count=concat_file_count,
                job_result=job_result,
                failure_reason=failure_reason,
                exception_type=exception_type,
            )
            self.logger.debug(f"Job ends.")

    @staticmethod
    def _get_exception_type():
        exc_type, exc_value, exc_traceback = sys.exc_info()
        return exc_type.__name__
