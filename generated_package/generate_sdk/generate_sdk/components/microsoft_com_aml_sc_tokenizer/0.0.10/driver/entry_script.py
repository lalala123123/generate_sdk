# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This is a helper module for users to use in entry script.
"""
import os
from pathlib import Path
import logging
from multiprocessing import current_process
import time

from singleton_meta import SingletonMeta
from utility import get_ip
from run_context_factory import RunContextFactory
from log_config import LogConfig


class EntryScript(metaclass=SingletonMeta):
    """This is a helper module for users to use in entry script."""

    def __init__(self, logging_level=None):
        self._logger = None
        self._logger_name = None
        self._log_dir = None
        self._output_dir = None
        self.run_context = RunContextFactory.get_context()
        self.logging_level = logging_level if logging_level else LogConfig().levelno
        self._entry_script_dir = str(Path(__file__).resolve().parents[1])

    def __reduce__(self):
        """ Declare what to pickle.
        """
        return (self.__class__, ())

    def config_log(self):
        """ Config logger to which will show up in run detail.
            Option: should we always config logger for users?
        """
        self._logger_name = f"{get_ip()}_{current_process().name}"
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)
        self._logger = logging.getLogger(self._logger_name)
        formatter = logging.Formatter(
            "%(asctime)s|%(name)s|%(levelname)s|%(process)d|%(thread)d|%(funcName)s()|%(message)s"
        )
        formatter.converter = time.gmtime
        self._logger.setLevel(self.logging_level)

        handler = logging.FileHandler(str(Path(self.log_dir) / f"{current_process().name}.txt"), delay=True)
        handler.setLevel(self.logging_level)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    @property
    def logger(self):
        """ Return a logger to write logs to users/ folder.
            The folder will show up in run detail in azure portal.
        """
        if self._logger is None:
            self.config_log()

        return self._logger

    @property
    def log_dir(self):
        """ The full path containing user logs"""
        if self._log_dir is None:
            self._log_dir = str(Path(self.run_context.working_dir) / "logs/user" / get_ip())
        return self._log_dir

    @property
    def dir(self):
        """ The full path containing entry script file."""
        return self._entry_script_dir

    @property
    def working_dir(self):
        """ The full path of the working directory when launching driver scripts.
            Then workers change to temp folder.
        """
        return self.run_context.working_dir

    @property
    def output_dir(self):
        """ The full path of the directory containg generated temp results and final result for 'append_row'.
            Users should also use this folder to store the output of their entry script.
            Users don't need to create this directory.
        """
        if self._output_dir is None:
            pth = Path(os.environ.get("AZUREML_BI_OUTPUT_PATH", "."))
            pth.mkdir(parents=True, exist_ok=True)
            self._output_dir = str(pth)

        return self._output_dir
