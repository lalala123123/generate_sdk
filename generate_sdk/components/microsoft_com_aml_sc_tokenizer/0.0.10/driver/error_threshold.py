# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides features of failure threshold control.
"""
import logger
from constant import Constant
from exception import ErrorThresholdException
from telemetry_logger import log_error


class ErrorThreshold:
    """ The class provides features of failure threshold control."""

    def __init__(self, allowed_failed_items):
        self.logger = logger.get_logger()

        self.allowed_failed_items = allowed_failed_items
        self.actual_failed_items = -1

    def exceeded(self):
        """ Return True if exceeding threshold.
        """
        if self.allowed_failed_items <= -1:
            return False

        return self.count_exceeded()

    def count_exceeded(self):
        """ Return True if exceeding allowed_failure_count
        """
        if self.actual_failed_items == -1:  # progress is not available yet.
            return False

        if self.actual_failed_items > self.allowed_failed_items:
            message = (
                f"The number of failed {Constant.TERM_ITEMS} is {self.actual_failed_items}, which exceeds "
                f"error threshold {self.allowed_failed_items}. Stopping processing. "
            )
            log_error(message)
            return True

        message = (
            f"The number of failed {Constant.TERM_ITEMS} is {0}, which doesn't exceed error threshold "
            f"{self.allowed_failed_items}. Continuing processing."
        )
        self.logger.debug(message)
        return False

    def check(self):
        """ Throw exception if exceeding error threshold
        """
        if self.exceeded():
            raise ErrorThresholdException(self.allowed_failed_items, self.actual_failed_items)
