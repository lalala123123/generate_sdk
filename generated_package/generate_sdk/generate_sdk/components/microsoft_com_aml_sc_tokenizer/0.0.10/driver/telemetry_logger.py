# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This module provides features to write telemetry and log."""
import os
import time
import uuid
import sys
import platform
import traceback
import requests
from run_context_factory import RunContextFactory
import utility
from logger import get_logger
from required_fields import RequiredFields
from standard_fields import StandardFields, AzureMLTelemetryComputeType
from telemetry_event import TelemetryEvent

MAX_POST_TIMES = 3
SLEEP_DURATION = 1
SERVICE_ENDPOINT = os.environ.get("AZUREML_SERVICE_ENDPOINT", "")
EXPERIMENT_SCOPE = os.environ.get("AZUREML_EXPERIMENT_SCOPE", "")
RUN_TOKEN = os.environ.get("AZUREML_RUN_TOKEN", "")
IS_URL_VALID = None  # None means not checked yet.


def get_default_headers(token, content_type=None, read_bytes=None):
    """ Get default headers."""
    headers = {"Authorization": "Bearer %s" % token}

    if content_type:
        headers["Content-Type"] = content_type

    if read_bytes:
        headers["Content-Length"] = "%d" % len(read_bytes)

    return headers


def try_request(url, json_payload, headers):
    """ Try to send request.
        It will sallow exceptions to avoid breaking callers."""
    logger = get_logger("Telemetry")
    for index in range(MAX_POST_TIMES):
        try:
            resp = requests.post(url, json=json_payload, headers=headers)
            resp.raise_for_status()
            return
        except requests.exceptions.HTTPError as http_err:
            if index == 0:
                logger.warning(f"Failed to send json payload log {json_payload}")
            logger.warning(
                f"Failed to send log with error {str(http_err)} response Code: {resp.status_code}, "
                f"Content: {resp.content}. Detail: {traceback.format_exc()}"
            )
            if resp.status_code >= 500:
                time.sleep(SLEEP_DURATION)
                logger.debug("Retrying...")
            else:
                return
        except BaseException as exc:
            logger.warning(f"Failed to send log: {json_payload} with error {exc}. Detail: {traceback.format_exc()}.")

            return


def is_url_valid():
    """ True if the url is valid."""
    # Use this flag to write warning only on the first failure.
    global IS_URL_VALID  # pylint: disable=global-statement

    logger = get_logger("Telemetry")

    run_id = RunContextFactory.get_context().run_id
    if IS_URL_VALID is None:  # has not checked yet
        if SERVICE_ENDPOINT == "" or EXPERIMENT_SCOPE == "" or run_id == "":
            # TODO: use actual URL validator
            execution_url = SERVICE_ENDPOINT + "/execution/v1.0" + EXPERIMENT_SCOPE + "/runs/" + run_id + "/"
            telemetry_url = execution_url + "telemetry"
            logger.warning(f"Telemetry url {telemetry_url} is incorrect or malformed")
            IS_URL_VALID = False
        else:
            IS_URL_VALID = True

    return IS_URL_VALID


def log_message_internal(level, log_locally, message, *args):
    """ Log all telemetry/logs on client side Python logging levels (
        https://docs.python.org/2/library/logging.html#logging-levels) are difference than one used in telemetry APIs (
        https://docs.microsoft.com/en-us/dotnet/api/microsoft.extensions.logging.loglevel?view=aspnetcore-2.2)
    """

    logger = get_logger("Telemetry")
    log_level = 20 if level == "Information" else 30 if level == "Warning" else 40
    if log_locally:
        logger.log(log_level, message, *args)

    run_id = RunContextFactory.get_context().run_id
    if is_url_valid():
        execution_url = SERVICE_ENDPOINT + "/execution/v1.0" + EXPERIMENT_SCOPE + "/runs/" + run_id + "/"
        telemetry_url = execution_url + "telemetry"

        payload = {
            "Level": level,
            "Message": message,
            "MessageContext": list(args),
            "AdditionalContext": {"attribution": "BatchInferencing"},
        }

        headers = get_default_headers(RUN_TOKEN, content_type="application/json")
        try_request(telemetry_url, payload, headers)


def log_message_internalV2(level, log_locally, required_fields, standard_fields=None, extension_fields=None):

    logger = get_logger("Telemetry")
    log_level = 20 if level == "Information" else 30 if level == "Warning" else 40
    if log_locally:
        logger.log(
            log_level,
            f"required_fields:{required_fields.__dict__}\n"
            f"standard_fields:{standard_fields.__dict__ if standard_fields else None}\n"
            f"extension_fields:{extension_fields}",
        )

    run_id = RunContextFactory.get_context().run_id
    if is_url_valid():
        execution_url = SERVICE_ENDPOINT + "/execution/v2.0" + EXPERIMENT_SCOPE + "/runs/" + run_id + "/"
        telemetry_url = execution_url + "telemetryV2"
        payload = TelemetryEvent(required_fields, standard_fields, extension_fields)
        headers = get_default_headers(RUN_TOKEN, content_type="application/json")

        try_request(telemetry_url, payload, headers)


def generate_required_fields(event_name):
    required_fields = RequiredFields(
        subscriptionId=os.environ.get("AZ_BATCHAI_JOB_SUBSCRIPTION_ID", None),
        workspaceId=os.environ.get("AZUREML_WORKSPACE_ID", None),
        correlationId=str(uuid.uuid4()),
        componentName="ParallelRunStep",
        eventName=event_name,
    )
    return required_fields


def generate_standard_fields():
    run_context = RunContextFactory.get_context()
    wks = run_context.workspace
    run = run_context.run
    standard_fields = StandardFields(
        Attribution="ParallelRunStep",
        WorkspaceRegion=wks.location,
        ComputeType=int(AzureMLTelemetryComputeType.BatchAI),
        ClientOS=sys.platform,
        ClientOSVersion=platform.platform(),
        RunId=run_context.run_id,
        ParentRunId=run.parent.id,
        ExperimentId=run_context.experiment_id,
    )
    return standard_fields


# LogLevel should match with one defined in
# https://docs.microsoft.com/en-us/dotnet/api/microsoft.extensions.logging.loglevel?view=aspnetcore-2.2
# Call below functions as
# log_*("Message {varName1} {varName2}", varName1Value, varName2Value)
# Above log call will added as below assuming varName1Value="Val1", varName2Value="Val2"
#     message column: "Message Val1 Val2"
#     customDimentioned: {varName1: Val1, varName2: Val2}
def log_info(message, *args):
    """ Write info log."""
    log_message_internal("Information", True, message, *args)


def log_warning(message):
    """ Write warning log."""
    new_message = message.replace("{", "[").replace("}", "]")
    log_message_internal("Warning", True, new_message)


def log_error(message):
    """ Write error log."""
    new_message = message.replace("{", "[").replace("}", "]")
    log_message_internal("Error", True, new_message)


def log_process_telemetry(
    start_time,
    end_time,
    duration,
    process_time,
    run_method_time,
    total_tasks,
    succeeded_tasks,
    total_items,
    succeeded_items,
):
    """ Send process telemetry.
        Telemetry message is constructed differently for client side logging and sending it to server side
        because python logging formatting is different that microsoft.extensions.logging.
        Server side telemetry formatted this way to make it easier for querying
    """
    process_id = os.getpid()
    start_time_str = utility.fmt_time(start_time)
    end_time_str = utility.fmt_time(end_time)
    log_message_internal(
        "Information",
        False,
        "Worker - Telemetry: hostIp:{hostIp}, processId:{processId}, computeType:{computeType}, "
        "startTime:{startTime}, endTime:{endTime}, duration:{duration}, processTime:{processTime}, "
        "runMethodTime:{scoringTime}, totalTasks:{totalTasks}, succeededTasks:{succeededTasks}, "
        "totalItems:{totalItems}, succeededItems:{totalItems}",
        utility.get_ip(),
        process_id,
        "AmlCompute",
        start_time_str,
        end_time_str,
        duration,
        process_time,
        run_method_time,
        total_tasks,
        succeeded_tasks,
        total_items,
        succeeded_items,
    )
    logger = get_logger("Telemetry")
    logger.info(
        f"Worker - Telemetry: hostIp:{utility.get_ip()}, processId:{process_id}, computeType:AmlCompute, "
        f"startTime:{start_time_str}, endTime:{end_time_str}, duration:{duration}, processTime:{process_time}, "
        f"scoringTime:{run_method_time}, totalTasks:{total_tasks}, succeededTask:{succeeded_tasks}, "
        f"totalItems:{total_items}, succeededItems:{succeeded_items}"
    )

    """ Send worker ParallelRunStep process end telemetry."""
    required_fields = generate_required_fields("ParallelRunStep.Process.End")
    standard_fields = generate_standard_fields()
    standard_fields.Duration = utility.timespan(int(duration))
    extension_fields = dict(
        {
            "StartTime": start_time_str,
            "EndTime": end_time_str,
            "HostIp": utility.get_ip(),
            "ProcessId": process_id,
            "ProcessTime": str(process_time),
            "RunMethodTime": str(run_method_time),
            "TotalTasks": str(total_tasks),
            "SucceededTasks": str(succeeded_tasks),
            "TotalItems": str(total_items),
            "SucceededItems": str(succeeded_items),
            "JobId": os.environ.get("AZ_BATCH_JOB_ID", ""),
        }
    )
    log_message_internalV2("Information", True, required_fields, standard_fields, extension_fields)


def log_node_telemetry(
    start_time,
    end_time,
    duration,
    number_of_cores,
    number_of_nodes,
    core_seconds,
):
    """Send node telemetry.

    Telemetry message is constructed differently for client side logging and sending it to server side
    because python logging formatting is different that microsoft.extensions.logging.
    Server side telemetry formatted this way to make it easier for querying
    """
    start_time_str = utility.fmt_time(start_time)
    end_time_str = utility.fmt_time(end_time)
    log_message_internal(
        "Information",
        False,
        "Worker - Telemetry: hostIp:{hostIp}, processId:{processId}, computeType:{computeType}, "
        "startTime:{startTime}, endTime:{endTime}, duration:{duration}",
        utility.get_ip(),
        os.getpid(),
        "AmlCompute",
        start_time_str,
        end_time_str,
        duration,
    )
    logger = get_logger("Telemetry")
    logger.info(
        f"Worker - Telemetry: hostIp:{utility.get_ip()}, computeType:AmlCompute, "
        f"startTime:{start_time_str}, endTime:{end_time_str}, duration:{duration}"
    )

    """ Send worker ParallelRunStep Job Worker Duration telemetry."""
    required_fields = generate_required_fields("ParallelRunStep.Node.Duration")
    standard_fields = generate_standard_fields()
    standard_fields.Duration = utility.timespan(int(duration))
    standard_fields.NumberOfCores = number_of_cores
    standard_fields.NumberOfNodes = number_of_nodes
    standard_fields.CoreSeconds = core_seconds
    extension_fields = dict(
        {
            "StartTime": start_time_str,
            "EndTime": end_time_str,
            "HostIp": utility.get_ip(),
            "JobId": os.environ.get("AZ_BATCH_JOB_ID", ""),
        }
    )
    log_message_internalV2("Information", True, required_fields, standard_fields, extension_fields)


def log_job_start_telemetry(
    input_format,
    output_action,
    mini_batch_size,
    process_count_per_node,
    error_threshold,
    client_sdk_version,
    aml_core_version,
    dataprep_version,
    number_of_nodes
):
    """Log the job start event."""
    required_fields = generate_required_fields("ParallelRunStep.Job.Start")
    standard_fields = generate_standard_fields()
    standard_fields.NumberOfNodes = number_of_nodes
    standard_fields.DatasetType = input_format
    extension_fields = dict(
        {
            "OutputAction": output_action,
            "MiniBatchSize": mini_batch_size,
            "ProcessCountPerNode": process_count_per_node,
            "ErrorThreshold": error_threshold,
            "ClientSdkVersion": client_sdk_version,
            "AmlCoreVersion": aml_core_version,
            "DataprepVersion": dataprep_version,
            "JobId": os.environ.get("AZ_BATCH_JOB_ID", ""),
        }
    )
    """ Send master ParallelRunStep Job Start telemetry."""
    log_message_internalV2("Information", True, required_fields, standard_fields, extension_fields)


def log_job_end_telemetry(
    start_time,
    end_time,
    duration,
    input_format,
    input_ds_count,
    output_action,
    mini_batch_size,
    process_count_per_node,
    error_threshold,
    number_of_nodes,
    first_task_creation_time,
    total_scheduling_time,
    total_tasks,
    total_items,
    processed_tasks,
    processed_items,
    failed_items,
    concat_file_time,
    concat_file_count,
    job_result,
    failure_reason,
    exception_type,
):
    """Log the job end event."""
    start_time_str = utility.fmt_time(start_time)
    end_time_str = utility.fmt_time(end_time)
    log_message_internal(
        "Information",
        False,
        "Master - Telemetry: hostIp:{hostIp}, computeType:{computeType}, "
        "startTime:{startTime}, endTime:{endTime}, duration:{duration}, "
        "inputFormat:{inputFormat}, inputDsCount:{inputDsCount}, "
        "completedTasks:{completedTasks}, completedCount:{completedCount}, failedCount:{failedCount}, "
        "totalCount:{totalCount}, outputAction:{outputAction}, "
        "miniBatchSize:{miniBatchSize}, processCountPerNode:{processCountPerNode}, "
        "errorThreshold:{errorThreshold}, numberOfNodes:{numberOfNodes}, jobResult:{jobResult}, "
        "failureReason:{failureReason}, exceptionType:{exceptionType}",
        utility.get_ip(),
        "AmlCompute",
        start_time_str,
        end_time_str,
        duration,
        input_format,
        input_ds_count,
        processed_tasks,
        processed_items,
        failed_items,
        total_tasks,
        output_action,
        mini_batch_size,
        process_count_per_node,
        error_threshold,
        number_of_nodes,
        job_result,
        failure_reason,
        exception_type,
    )
    logger = get_logger("Telemetry")
    logger.info(
        f"Master - Telemetry: hostIp:{utility.get_ip()}, computeType:AmlCompute, "
        f"startTime:{start_time_str}, endTime:{end_time_str}, duration:{str(duration)}, "
        f"inputFormat:{input_format}, inputDsCount:{input_ds_count}, "
        f"processedTasks:{processed_tasks}, processedItems:{processed_items}, failedItems:{failed_items}, "
        f"totalTasks:{total_tasks}, totalItems:{total_items}, "
        f"outputAction:{output_action}, "
        f"miniBatchSize:{mini_batch_size}, processCountPerNode:{process_count_per_node}, "
        f"errorThreshold:{error_threshold}, numberOfNodes:{number_of_nodes}, jobResult:{job_result}, "
        f"failureReason:{failure_reason}, exceptionType:{exception_type}"
    )

    required_fields = generate_required_fields("ParallelRunStep.Job.End")
    standard_fields = generate_standard_fields()
    standard_fields.Duration = utility.timespan(int(duration))
    standard_fields.TaskResult = job_result
    standard_fields.FailureReason = failure_reason
    standard_fields.NumberOfNodes = number_of_nodes
    standard_fields.DatasetType = input_format
    extension_fields = dict(
        {
            "StartTime": start_time_str,
            "EndTime": end_time_str,
            "InputDatasetCount": input_ds_count,
            "OutputAction": output_action,
            "MiniBatchSize": mini_batch_size,
            "ProcessCountPerNode": process_count_per_node,
            "ErrorThreshold": error_threshold,
            "FirstTaskCreationTime": first_task_creation_time,
            "TotalSchedulingTime": total_scheduling_time,
            "TotalTasks": total_tasks,
            "TotalItems": total_items,
            "ProcessedTasks": processed_tasks,
            "ProcessedItems": processed_items,
            "FailedItems": failed_items,
            "ConcatFileTime": concat_file_time,
            "ConcatFileCount": concat_file_count,
            "JobId": os.environ.get("AZ_BATCH_JOB_ID", ""),
        }
    )
    """ Send master ParallelRunStep Job End telemetry."""
    log_message_internalV2("Information", True, required_fields, standard_fields, extension_fields)


def log_task_manager_telemetry(mini_batch_count, total_items, init_duration, first_task_duration, queue_time):
    """ Write task manager telemetry."""
    log_message_internal(
        "Information",
        False,
        "Master - Task queue job completed: Scheduled {miniBatchCount} mini batches with {totalItems} items. "
        "Provider init time: {initDuration}, first task creation time: {firstTaskDuration}, "
        "total queue time: {queueTime}.",
        mini_batch_count,
        total_items,
        init_duration,
        first_task_duration,
        queue_time,
    )
    logger = get_logger("Telemetry")
    logger.info(
        f"Master - Task queue job completed: Scheduled {mini_batch_count} mini batches with {total_items} items. "
        f"Provider init time: {init_duration}, first task creation time: {first_task_duration}, "
        f"total queue time: {queue_time}."
    )
