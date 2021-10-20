# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This module defines exceptions.
"""

from constant import Constant
from enum import IntEnum


class ExceptionCategory(IntEnum):
    """Define the category of exception."""

    User = 1  # Caused by error in the entry script
    Driver = 2  # Caused by driver code
    Dependency = 3  # Caused by dependencies, such as dataset, azure storage.

    def __str__(self):
        """Return the text."""
        return super().__str__().split(".")[1]


class InputFileNotFoundError(FileNotFoundError):
    """Error for an agent cannot find an input from a task.

    This error occurs on agent side only.
    Possible causes:
    1. a node doesn't mount the input correctly. This is a system error.
    2. connectivity issues. This is an dependency error.
    3. users delete the source files. This is a user error.

    Consider this as system error we think  1 and 2 are major ones.
    """

    def __init__(self, *args, category: ExceptionCategory = ExceptionCategory.User, **kwargs):
        """Init the category."""
        self.category = category
        super().__init__(
            *args, **kwargs,
        )


class UserInputNotFoundError(Exception):
    """Exception for unable to read user input.

    Consider this as a user error.
    """


class NoResultToAppendError(Exception):
    """There is no process result returned from run().

    This is from append_row only.
    Consider this as a user error.
    """


class EntryScriptException(Exception):
    """Exception from the entry script."""


class DriverException(Exception):
    """Exception from the driver script."""


class UserException(Exception):
    """ Exception that will raise to end users.
        It will show up in the run page in azure portal.

        The message needs to clearly describe:
            1) The cause.
            2) What actions the user can do next.
    """

    ACTIONS = ["Please check logs for error. You can check logs/readme.txt for the layout of logs."]

    def __init__(self, cause):
        self.cause = cause
        super().__init__()

    def __str__(self):
        """ Return the string representation of this instance."""
        return self.cause + "\n" + "\n".join(self.ACTIONS)


class FirstTaskCreationTimeout(UserException):
    """ Unable to create any task within the allowed time."""

    ACTIONS = [
        "Reduce the single input size or "
        "set the advanced argument '--first_task_creation_timeout' to a larger value in arguments in ParallelRunStep.",
    ]

    def __init__(self, timeout):
        super().__init__(f"Unable to create any task within {timeout} seconds.")


class TaskCreationException(UserException):
    """ Failed to create a task."""

    ACTIONS = ["Please check logs/overview.txt and logs/master.txt for error."]

    def __init__(self, failed_tasks, exceptions):
        super().__init__(f"Failed to create tasks {failed_tasks} with {exceptions}.")


class NoTaskPickedException(UserException):
    """ There is no pending tasks.
        Workers don't report any task picked back to the master.
    """

    ACTIONS = ["Check worker logs for errors."]

    def __init__(self):
        super().__init__("No task has been picked.")


class NoTaskProcessedException(UserException):
    """ There are pending tasks, but no processed task.
    """

    ACTIONS = [
        "Check logs/report/pending_tasks.csv if there is any task has been picked.",
        "Check worker logs for error messages.",
    ]

    # TODO: add pending and poisoned count
    # def __init__(self, pending_count, poisoned_count):
    # if processed_count > 0:
    #     message = (
    #         f"There are {pending_count} pending tasks which can be found in logs/report/pending_tasks.csv"
    #         f" and {processed_count} processed tasks which can be found in logs/report/processed_tasks.csv."
    #     )
    # else:
    #     if pending_count > 0:
    #         message = (
    #             "No task was processed."
    #             f" There are {pending_count} pending tasks which can be found in logs/report/pending_tasks.csv"
    #         )

    def __init__(self):

        super().__init__("No task has been processed.")


class SomeTaskProcessedException(UserException):
    """ Some task processed.
    """

    # TODO: add pending and poisoned count

    ACTIONS = [
        "Check logs/report/processed_tasks.csv for the process time for finished task.",
        "If the processed time is more than run_invocation_timeout, increase run_invocation_timeout"
        " in ParallelRunConfig to a larger value and try again.",
        "If all processed time are not more than run_invocation_timeout, check worker logs.",
    ]

    def __init__(self, pending_count, processed_count):
        assert pending_count >= 0
        if processed_count <= 0:
            raise ValueError(f"Invalid processed_count {processed_count}. It must be a non-negative int.")

        if pending_count > 0:
            message = (
                f"There are {pending_count} pending tasks which can be found in logs/report/pending_tasks.csv"
                f" and {processed_count} processed tasks which can be found in logs/report/processed_tasks.csv."
            )
        else:
            message = " There is no pending tasks."

        super().__init__(message)


class ErrorThresholdException(UserException):
    """ There is at least one task processed, but hitting error threshold. """

    # TODO: add the allowed failed items and actual failed items.
    ACTIONS = [
        "Check logs/report/processed_tasks.csv for the process time for finished task.",
        "If the processed time is more than run_invocation_timeout, increase run_invocation_timeout"
        " in ParallelRunConfig to a larger value and try again.",
        "If all processed time are not more than run_invocation_timeout, check worker logs.",
    ]

    def __init__(self, allowed_failed_items, actual_failed_items):
        message = (
            f"The number of failed {Constant.TERM_ITEMS} is {actual_failed_items}, which exceeds error "
            f"threshold {allowed_failed_items}."
        )
        super().__init__(message)


class TaskPoisonedException(UserException):
    """ There are message poisoned"""

    ACTIONS = [
        "Check worker logs for error message.",
        "Increase run_invocation_timeout in ParallelRunConfig to a larger value and try again.",
    ]

    def __init__(self, pending_count, processed_count):
        if processed_count > 0:
            message = (
                f"There are {pending_count} pending tasks which can be found in logs/report/pending_tasks.csv"
                f" and {processed_count} processed tasks which can be found in logs/report/processed_tasks.csv."
            )
        else:
            message = (
                f"There are {pending_count} pending tasks which can be found in logs/report/pending_tasks.csv."
                f" No task was processed."
            )
        super().__init__(message)


class UnknownException(UserException):
    """ The exception should not happen, which means bugs in code."""

    ACTIONS = ["Please check logs/overview.txt, logs/master.txt and worker logs for error."]

    def __init__(self):
        message = "Unknown error happened."
        super().__init__(message)
