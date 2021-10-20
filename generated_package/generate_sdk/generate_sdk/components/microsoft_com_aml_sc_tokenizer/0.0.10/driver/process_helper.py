# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This module provides helper features for process management.
"""
import os
from pathlib import Path
import traceback
import psutil

from constant import Message
import logger
from telemetry_logger import log_warning
from run_context_factory import RunContextFactory


class ProcessHelper:
    """ This class provides helper features for process management."""

    def __init__(self):
        self.logger = logger.get_logger()
        self.run_context = RunContextFactory.get_context()
        self.pid_dir = self.get_pid_dir()

    def get_pid_dir(self):
        """ Return a local folder containing the pid files."""
        pid_dir = Path(self.run_context.temp_dir) / "pid"
        pid_dir.mkdir(parents=True, exist_ok=True)
        return str(pid_dir)

    def write_pid(self, pid):
        """ Create an empty file with the pid as file name."""
        with open(os.path.join(self.pid_dir, f"{pid}"), "w"):
            pass

    def delete_pid(self, pid):
        """ Delete a pid file."""
        try:
            os.remove(os.path.join(self.pid_dir, f"{pid}"))
        except FileNotFoundError:
            pass  # This can be deleted by other process.

    def kill_pid(self, pid):
        """ Try to kill a process and swallow exception if failed"""
        try:
            self.logger.info(f"kill process {pid}.")
            proc = psutil.Process(pid)
            proc.terminate()
        except psutil.NoSuchProcess:
            self.logger.debug(f"No such process {pid}. The process exits before kill.")
        except BaseException as exc:
            self.logger.warning(
                Message.FAILED_ACTION_WITH_ERROR_DETAIL.format(
                    f"failed to kill process {pid}", exc, traceback.format_exc()
                )
            )

    def get_pids(self):
        """ Return a list of the pids."""
        return [int(s) for s in os.listdir(self.pid_dir)]

    def kill(self):
        """ Kill all processes other than the current one. """
        current_pid = os.getpid()

        for pid in os.listdir(self.pid_dir):
            pid = int(pid)
            if pid != current_pid:
                self.kill_pid(pid)
                self.delete_pid(pid)

    def nice(self, pid=None, nice=None):
        """ Set or get the niceness of the process.
            If the parameter pid is None, current process will be used.
            If nice is None, return the nice.

            Set nice is only supported on Linux platform. It will be ignored on other platforms.
            This method will only increase the niceness.
            It will ignore if the parameter nice is not greater than the current nice.
        """
        if pid is None:
            process = psutil.Process()
        else:
            process = psutil.Process(pid)

        current_nice = process.nice()

        self.logger.debug(f"pid={pid}, current nice={current_nice}, new nice={nice}")

        if nice is None:
            return current_nice

        if psutil.LINUX:
            if current_nice < nice:
                process.nice(nice)
                self.logger.info(Message.CHANGED_NICE.format(current_nice, nice))
