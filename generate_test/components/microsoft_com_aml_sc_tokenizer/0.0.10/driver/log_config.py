# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides features to config log.

Seperate this from logger.py to avoid cyclic reference.
This module needs run_context for working directory, and the latter needs logger for logging.
"""
import logging
from multiprocessing import current_process
import os
from pathlib import Path
import time

from constant import Constant
from singleton_meta import SingletonMeta
from run_context_factory import RunContextFactory
from utility import get_ip
from custom_file_handler import CustomFileHandler


class LevelFilter(logging.Filter):
    """ Only keeping the specified level."""

    def __init__(self, levels):
        super().__init__()
        self.levels = levels

    def filter(self, record):
        """ Return True if in the list."""
        return record.levelno in self.levels


class LogConfig(metaclass=SingletonMeta):
    """ The class for log config."""

    def __init__(self):
        self.log_dir = self.get_log_dir()
        self.levelno = logging.INFO
        self.is_master = True
        self.configured = False

    def get_log_dir(self):
        """ Return the folder for user and sys logs.
            Files and folders in it will be uploaded and show up in run detail page in the azure portal.
        """
        working_dir = RunContextFactory.get_context().working_dir
        log_dir = os.path.join(working_dir, "logs")
        return log_dir

    def clear_file_hanlder(self, logger):
        """ Remove all file handlers from the logger."""
        file_handlers = []
        for handler in logger.handlers:
            if isinstance(handler, CustomFileHandler):
                file_handlers.append(handler)

        for handler in file_handlers:
            logger.handlers.remove(handler)

    def get_formatter(self, level):
        """ Return a formatter."""
        if level <= logging.DEBUG:
            fmt = "%(asctime)s|%(name)s|%(levelname)s|%(process)d|%(thread)d|%(funcName)s()|%(message)s"
        else:
            fmt = "%(asctime)s|%(name)s|%(levelname)s|%(process)d|%(message)s"

        formatter = logging.Formatter(fmt)
        formatter.converter = time.gmtime

        return formatter

    def get_file_hanlder(self, file_path, level):
        """ Return a file handler."""
        handler = CustomFileHandler(filename=file_path, mode="a", maxBytes=0, backupCount=0, encoding=None, delay=True)
        handler.setLevel(level)
        handler.setFormatter(self.get_formatter(level))
        return handler

    def get_files(self):
        """ Return the full paths of files."""
        if self.is_master:
            files = [f"sys/{Constant.MASTER_LOG_FILE_NAME}", "sys/warning.txt", "sys/error.txt", "user/error.txt"]
        else:

            file_name = f"{current_process().name}.txt"
            ip_addr = get_ip()

            files = [
                f"sys/worker/{ip_addr}/{file_name}",
                f"sys/warning/{ip_addr}/{file_name}",
                f"sys/error/{ip_addr}/{file_name}",
                f"user/error/{ip_addr}/{file_name}",
            ]

        return [str(Path(self.log_dir) / f) for f in files]

    def get_task_file(self):
        """Return the file to save tasks."""
        return Path(self.log_dir) / "sys/worker/" / get_ip() / f"{current_process().name}.task.csv"

    def config_loggers(self):
        """ Config the loggers for a master role."""
        if self.configured:
            return

        logger = logging.getLogger(Constant.TERM_TOP_LOG_NAME)
        logger.propagate = False
        logger.setLevel(self.levelno)

        files = self.get_files()

        self.clear_file_hanlder(logger)
        levels = [self.levelno, logging.WARNING, logging.ERROR, logging.ERROR]

        for i in range(3):
            handler = self.get_file_hanlder(files[i], levels[i])
            if i == 1:
                handler.addFilter(LevelFilter([logging.WARNING]))
            logger.addHandler(handler)

        logger = logging.getLogger(Constant.USER_ERROR_LOG_NAME)
        logger.setLevel(logging.ERROR)
        logger.addHandler(self.get_file_hanlder(files[3], levels[3]))
        logger.propagate = False

        self.configured = True

    def config(self, level, is_master=True):
        """ Config loggers for workers.
            Each process needs to call this once.
        """
        if isinstance(level, int):
            self.levelno = level
        elif isinstance(level, str):
            self.levelno = logging.getLevelName(level)
        else:
            raise ValueError(f"Invalid level '{level}'.")

        self.is_master = is_master
        if is_master:
            self.readme()

        self.config_loggers()

    def config_overview(self):
        """ Config the overview logger."""
        log_dir = self.get_log_dir()

        formatter = logging.Formatter("%(asctime)s|%(levelname)s|%(message)s")
        formatter.converter = time.gmtime

        logfilename = os.path.join(log_dir, Constant.OVERVIEW_LOG_FILE_NAME)
        level = "INFO"
        handler = CustomFileHandler(filename=logfilename, maxBytes=1024 * 100, backupCount=100)
        handler.setLevel(level)
        handler.setFormatter(formatter)

        logger = logging.getLogger(Constant.OVERVIEW_LOG_NAME)
        logger.setLevel(level)
        logger.propagate = False  # Don't write to ancestor logs.

        self.clear_file_hanlder(logger)
        logger.addHandler(handler)

    def readme(self):
        """ Write readme.txt """
        log_guide = """About the logs folder:
logs/
  azureml/    : azureml logs
  user/       : Including errors and logs from users.
    error/    : Error from input, entry script validation or running.
    log/      : The logs from entry script using entry script helper.
  sys/        : sys error folder.
    error/    : error logs
    perf/     : node and process resource usages, each node has a sub folder.
                Check sys.csv for the resource usages of the node.
                Check other files for the resource usages of a process.
                Try a larger VM size or more nodes.
                Reduce the value of --process_count_per_node if it's larger than 1.
    report/     : processed tasks, pending tasks and override tasks
    worker/     : logs from workers. each node has a sub folder
        <node ip>
            MainProcess.txt     : main process
            Process-1.task.csv  : Tasks picked and processed by Process-1
            Process-1.txt       : Logs of Process-1
    warning/    : warning logs
    master.txt  : the master logs, including task creation, progress monitoring, run result.
    overview.txt: high level progress.
    poison_task  : if there is any poison task, this file will show up.
    """
        log_dir = Path(self.get_log_dir())
        log_dir.mkdir(parents=True, exist_ok=True)
        file_path = str(log_dir / "readme.txt")
        with open(file_path, "w") as fil:
            fil.write(log_guide)
