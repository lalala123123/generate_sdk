# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" The module provides features to run command in shell."""
import os
from threading import Thread
import subprocess
import traceback
import psutil

from constant import Message
from job_state import JobState
from logger import get_logger
from telemetry_logger import log_error


class ShellExec:
    """ This class provides features to run command in shell.
    """

    def __init__(self):
        self.logger = get_logger()
        self.processes = []
        self.session_threads = []

    def run(self, command):
        """ Run the command."""
        self.logger.debug(f"start to run command: {command}.")

        if not isinstance(command, list):
            command = [command]

        proc = psutil.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd(),
            universal_newlines=True,
        )
        self.processes.append(proc)
        self.log_result(proc)

        return proc

    def restart_on_failure(self, command):
        """ Run the command and keep restarting on failure until got job stop signal."""
        while True:
            proc = self.run(command)

            if proc.returncode == 0:
                self.logger.info(f"{command} finished without error.")
                break
            if JobState().stopping():
                self.logger.info(f"{command} got job stop signal.")
                break

            self.logger.warning(f"Restart {command} for prior call exit with error code {proc.returncode}.")

    def log_result(self, proc):
        """Log the result of a terminiated process."""

        stdout, stderr = proc.communicate()
        stdout = stdout.strip()
        stderr = stderr.strip()

        self.logger.info(f"Process {proc.pid} returned with returncode {proc.returncode}. Args: {proc.args}.")
        if stdout:
            self.logger.info(f"stdout: {stdout}")
        if stderr:
            self.logger.warning(f"stderr: {stderr}")

    def run_async(self, command):
        """ Run a command in a new thread.
        """
        self.logger.debug(f"Start to run the command in a new thread.")
        thr = Thread(target=self.restart_on_failure, args=(command,))
        thr.start()
        self.session_threads.append(thr)

    def wait(self):
        """ Wait until all processes/threads end."""
        for thr in self.session_threads:
            try:
                self.logger.debug("Before join().")
                thr.join()
                self.logger.debug("After join().")
            except BaseException as exc:
                message = Message.FAILED_TO_JOIN_THREAD.format(exc, traceback.format_exc())
                self.logger.error(message)
                raise exc
