# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This module defines constants.
"""


class Constant:
    """ Define system wide constants.
    """

    PENDING_TASK_QUEUE_PREFIX = "prs1"
    PROCESSED_TASK_QUEUE_PREFIX = "prs2"
    QUEUE_PREFIXES = [PENDING_TASK_QUEUE_PREFIX, PROCESSED_TASK_QUEUE_PREFIX]

    DEFAULT_APPEND_ROW_FILE_NAME = "parallel_run_step.txt"

    EXIT_CODE_PROCESS_TIMEOUT = 71  # A task cannot finish within the time limit
    EXIT_CODE_SCORE_INIT_FAILED = 72
    EXIT_CODE_SCORE_RUN_SOME_FAILED = 73
    EXIT_CODE_SCORE_RUN_ALL_FAILED = 74
    EXIT_CODE_STOPPED = 82  # Being called to exit thread or process of the job.

    EXIT_CODES_START_NEW_PROCESS = [
        EXIT_CODE_PROCESS_TIMEOUT,
        EXIT_CODE_SCORE_INIT_FAILED,
        EXIT_CODE_SCORE_RUN_SOME_FAILED,
        EXIT_CODE_SCORE_RUN_ALL_FAILED,
    ]

    TERM_PRODUCT_NAME = "ParallelRunStep"
    TERM_MINI_BATCH = "mini batch"
    TERM_MINI_BATCHES = "mini batches"
    TERM_ITEM = "item"
    TERM_ITEMS = "items"
    TERM_TOP_LOG_NAME = TERM_PRODUCT_NAME
    TERM_PROGRESS_LOG_NAME = f"{TERM_TOP_LOG_NAME}.progress"

    MASTER_LOG_FILE_NAME = "master.txt"
    OVERVIEW_LOG_NAME = f"Overview"
    OVERVIEW_LOG_FILE_NAME = "overview.txt"

    MAX_AZURE_QUEUE_DELAY = 5  # A message sent to azure queue must be available for a consumer within the time range.

    USER_ERROR_LOG_NAME = f"{TERM_PRODUCT_NAME}.User Error"


class Message:  # pylint: disable=too-few-public-methods
    """ Define messages and message templates.
        The first step is to define all messages for INFO, WARNING and ERROR.
    """

    # 0: action
    # 1: brief error, like the string representation of an exception.
    FAILED_ACTION_WITH_ERROR = "Failed to {0} with {1}."

    # 0: same as FAILED_ACTION_WITH_ERROR
    # 1: same as FAILED_ACTION_WITH_ERROR
    # 2: the exception detail with stack trace
    FAILED_ACTION_WITH_ERROR_DETAIL = "Failed to {0} with {1}. Error detail: {2}"

    # 0: brief error, like the string representation of an exception.
    # 1: the exception detail with stack trace
    FAILED_TO_JOIN_THREAD = "Failed to join thread with {0}. Error detail: {1}"

    # 0: the name of the purpose of the thread
    THREAD_START = "Start thread to {0}."

    # 0: the name of the purpose of the thread
    THREAD_END = "The thread {0} ends."

    # 0: addtional details if needed
    LEAKED_QUEUE_CLEANUP_END = "Leaked queue cleanup finished.{0}"

    LEAKED_QUEUE_CLEANUP_END_NO_LEAKED_FOUND = "Leaked queue cleanup finished. No leaked queue found."

    # 0, created task count
    # 1, processed task count
    PROCESSED_MORE_THAN_CREATED = (
        f"Scheduled {{0}} {Constant.TERM_MINI_BATCHES}, processed {{1}} distinct {Constant.TERM_MINI_BATCHES}"
        "This should not happen. Please check log for errors"
    )

    # 0, created task count
    ALL_TASKS_RPOCESSED = f"All {{0}} {Constant.TERM_MINI_BATCHES} have been processed."

    # 0, additional summary.
    FINISHED_PROCESSED_ALL = f"The {Constant.TERM_PRODUCT_NAME} processed all {Constant.TERM_MINI_BATCHES}. {{0}}"
    FINISHED_WARNING_PROCESSED_MORE_THAN_CREATED = (
        f"The {Constant.TERM_PRODUCT_NAME} execution finished with warning."
        " The processed items is more than the input items. "
        "This is usually caused by race conditions or process/thread delays caused by one input item being "
        "processed more than once. There may be duplicated results in the output."
    )

    # 0, additional info.
    GOT_STOP_SIGNAL = f"Received stop signal and the {Constant.TERM_PRODUCT_NAME} is stopping.{{0}}"

    # 0, the round the polling
    EXCEEDED_MAX_ERROR_COUNT = "Exceeded the max error count on round {0}. Please check prior logs for cause."

    # 0, task id
    # 1, allowed timeout
    PROCESS_TIMEOUT = f"{Constant.TERM_MINI_BATCH} {{0}} did not finish in {{1}} seconds. Stopping this process."

    # 0, task id
    PROCESS_ABORTED = f"Process abort with unfinished {Constant.TERM_MINI_BATCH} {{0}}."

    # 0, wait time in seconds
    LONG_WAIT_IN_GET_TASKS = (
        "Wait {0} seconds to get a task."
        " This is usually caused by slow scheduling."
        " Please check log to see if there is any error."
    )

    # 0, wait time in seconds
    LONG_WAIT_FOR_FIRST_TASK_CREATION = (
        "First task creation is taking longer than {0} seconds."
        " This is usually caused by slow data source initialization."
        " Please cancel the job manually if you do not want to wait any longer."
    )

    STOP_REASON_GOT_STOP_SIGNAL = "Got stop signal."
    STOP_REASON_SET_STOPPING = "Master sent a stop signal."
    STOP_REASON_ERROR_THRESHOLD = "Exceeded error threshold."
    # 0, progress_update_timeout
    STOP_REASON_PROGRESS_TIMEOUT = "No progress update in {0} seconds."

    NO_SOURCE_FILE_ERROR = (
        "No temp file found. The job failed."
        " A job should generate temp files or should fail before this. Please check logs for the cause."
    )
    ALL_SOURCE_FILE_ARE_EMPTY = "All temp files are empty."

    # 0, the number of concatneated files
    # 1, the total number of files
    # 2, used time
    # 3, remaining time
    CONCAT_PROGRESS = "Concatenated {0}/{1} files in {2}. Estimated remaining {3}."

    # 0, the number of concatneated files
    # 1, the total number of files
    # 2, used time
    CONCAT_FINISHED = "Finished concatenating {0} files in {1}."

    CONCAT_FAILED = (
        "Concatenated {0}/{1} files in {2}."
        " Failed temp files were kept. You can download the folder to concatenate manually."
    )

    # 0, current nice
    # 1, new nice
    CHANGED_NICE = "Changed nice from {0} to {1}."

    # 0, total number of temp files
    # 1, total size in MB
    TOTAL_FILES_TO_CONCAT = "There are {0} temp files to concatenate. Total size is {1} MB."
