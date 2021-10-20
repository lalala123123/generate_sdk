# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This module defines exceptions caused by the entry script.
    All these exceptions should be resolved:
        1) by changing the entry script code.
        2) by increasing the timeout setting.
"""


class EntryScriptException(Exception):
    """ Represents an exception caused by the entry script."""


class EntryScriptInitException(EntryScriptException):
    """ The init() method raises an exception.
        The monitor reports this to the master, and exits worker process with the corresponding code.
    """


class EntryScriptInitTimeout(EntryScriptException):
    """ The init() method doesn't return in the allowed time.
        The monitor reports this to the master, and exits worker process with the corresponding code.
    """


class EntryScriptRunException(EntryScriptException):
    """ The run() method raises an exception.
        The monitor reports this to the master, and exits worker process with the corresponding code.
    """


class EntryScriptRunTimeout(EntryScriptException):
    """ The run() method doesn't return in the allowed time.
        The monitor reports this to the master, and exits worker process with the corresponding code.
    """


class EntryScriptRunReturnWrongType(EntryScriptException):
    """ The run() method doesn't a Pandas DataFrame or a list.
    """

    ACTIONS = [
        "The run() method doesn't return a Pandas DataFrame or a list.",
        "Please verify your entry script. run() method should return a Pandas DataFrame or a list."
        " For append_row output_action, these returned elements are appended into the common output file."
        " For summary_only, the contents of the elements are ignored."
        " For all output actions, each returned output element indicates one successful inference of input element"
        " in the input mini-batch.",
    ]

    def __init__(self, result):
        self.result = result
        super().__init__()

    def __str__(self):
        """ Return the string representation of this instance."""
        message = f"The return value '{self.result}' is not a Pandas DataFrame or a list.\n" + "\n".join(self.ACTIONS)
        return message


class EntryScriptShutdownException(EntryScriptException):
    """ The shutdown() method raises an exception.
        The monitor reports this to the master, and exits worker process with the corresponding code.
    """


class EntryScriptShutdownTimeout(EntryScriptException):
    """ The shutdown() method doesn't return in the allowed time.
        The monitor reports this to the master, and exits worker process with the corresponding code.
    """
