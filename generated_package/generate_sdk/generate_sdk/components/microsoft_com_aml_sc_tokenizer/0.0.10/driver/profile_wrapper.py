# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""This module provides a wrapper of Python built-in profile modules."""
import cProfile
import profile

import logger


class ProfileWrapper:
    """A wrapper of built-in profile modules."""

    def __init__(self, profiling_module):
        assert profiling_module in ["cProfile", "profile"], f"'{profiling_module}'' should be 'cProfile' or 'profile'."
        self.logger = logger.get_logger()
        if profiling_module == "cProfile":
            self.module = cProfile
        else:
            self.module = profile

    def runctx(self, statement, _globals, _locals, filename):
        """Call underlier runctx"""
        self.logger.info(f"Starting profiling with {self.module}. The output is {filename}.")
        self.module.runctx(statement, _globals, _locals, filename)
