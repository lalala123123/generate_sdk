# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides features to validate and load score module.
"""
import importlib
import sys
from os import path
from inspect import signature

from logger import get_logger
from telemetry_logger import log_error


class ScoreModule:
    """ The class represents a entry script module."""

    INVALID_MODULE = "Score module {0}.py is invalid for {1}."

    def __init__(self, name):
        """ Init this class.
            :param str name: the name of the score module, i.e., the base part of the entry script.
        """
        self.logger = get_logger()
        self.name = name
        self.module = None
        self.init = None
        self.run = None
        self.shutdown = None

    def validate_init(self):
        """ Validate the init() method if exists."""
        if hasattr(self.module, "init"):
            sig = signature(self.module.init)
            if sig.parameters:
                raise ValueError(
                    f"The method init() in the entry script {self.name} has incorrect signature {sig}."
                    " It should not have any parameter.\n"
                    " If you want to pass parameters to your entry script,"
                    " please specify them in 'arguments' in ParallelRunStep."
                    " And then get the parameters using argparse.\n"
                    " Please check help doc for the example."
                )

    def validate_run(self):
        """ Validate the run() method."""
        if not hasattr(self.module, "run"):
            message = self.INVALID_MODULE.format(self.name, "missing run()")
            self.logger.error(message)
            raise ValueError(message)

        sig = signature(self.module.run)
        if len(sig.parameters) != 1:
            raise ValueError(
                f"The method run() in the entry script {self.name} has incorrect signature {sig}."
                " It should not have exact one parameter.\n"
                " If you want to pass additional parameters to your entry script,"
                " please specify them in 'arguments' in ParallelRunStep."
                " And then get the parameters using argparse.\n"
                " Please check help doc for the example."
            )

    def validate_shutdown(self):
        """ Validate the shutdown() method if exists."""
        if hasattr(self.module, "shutdown"):
            sig = signature(self.module.shutdown)
            if sig.parameters:
                raise ValueError(
                    f"The method shutdown() in the entry script {self.name} has incorrect signature {sig}."
                    " It should not have any parameter.\n"
                    " If you want to pass parameters to your entry script,"
                    " please specify them in 'arguments' in ParallelRunStep."
                    " And then get the parameters using argparse.\n"
                    " Please check help doc for the example."
                )

    def validate(self):
        """ Validate methods of the score module."""
        self.validate_init()
        self.validate_run()
        self.validate_shutdown()

    def import_module(self):
        """ Import the module."""
        self.set_sys_path()
        self.module = importlib.import_module(self.name)
        self.validate()

        if hasattr(self.module, "init"):
            self.init = self.module.init

        self.run = self.module.run

        if hasattr(self.module, "shutdown"):
            self.shutdown = self.module.shutdown

    def set_sys_path(self):
        """ Add the folder containing user score scripts to search paths.
            In production, driver scripts are placed in "driver" folder
            under the folder containing the entry script.
        """
        abs_path = path.abspath(__file__)
        entry_script_dir = path.realpath(path.join(abs_path, "..", ".."))
        self.logger.debug(f"The folder containing entry script folder is {entry_script_dir}")
        if entry_script_dir not in sys.path:
            sys.path.insert(0, entry_script_dir)
            self.logger.debug(f"sys.path is changed to {sys.path}")
