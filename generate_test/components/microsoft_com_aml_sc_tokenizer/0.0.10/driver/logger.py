# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides logging related features.
"""
import inspect
import logging
from constant import Constant


def get_logger(name=None):
    """ Get logger by the name.
        If the name is None, defaults to the caller class name.
        Note that the name will be added a prefix.
        Use a prefix so that the setting won't impact root logger.
    """
    if name is None:
        stack = inspect.stack()
        caller_class_name = type(stack[1][0].f_locals["self"]).__name__
        name = caller_class_name

    return logging.getLogger(f"{Constant.TERM_TOP_LOG_NAME}.{name}")


def get_user_error_logger():
    """ Return a log for user error."""
    return logging.getLogger(Constant.USER_ERROR_LOG_NAME)


def keep(_id):
    """ Return True to indicate the caller should write log for the id.
        The goal is to keep a reasonable logs for repeating actions.
        This keeps 1..9, 10,20,...,90,...
        :param id, should be a sequential number.
    """
    return str(_id)[1:].replace("0", "") == ""
