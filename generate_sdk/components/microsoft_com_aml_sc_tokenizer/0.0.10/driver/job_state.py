# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides a shared job state across all processes.
"""
import os
import sys
import traceback
from pathlib import Path
import azure.common

import logger
from azure_queue_helper import AzureQueueHelper
from constant import Constant, Message
from telemetry_logger import log_info, log_warning, log_error
from run_context_factory import RunContextFactory


class JobState:
    """ Provides features to send messages to and receives from a global state store.
        This enable communication to all other nodes, processes or threads.
        So far, it only provides feature to send and receive job stop signal.
        See ../Readme.md for more details about stop conditions.
    """

    def __init__(self):
        self.logger = logger.get_logger()

        self.run_context = RunContextFactory.get_context()
        job_dir = Path(self.run_context.working_dir) / "job"
        self.stop_signal_file = str(job_dir / "stop_signal.txt")

        os.makedirs(str(job_dir), exist_ok=True)

    def add_reason(self, reason):
        """ Save the reason to send stop signal.
            In normal case, there should be only one reason.
            If sign_stop() is called again, a reason will be append to the file.
            This is for troubleshooting.
        """
        with open(self.stop_signal_file, "a") as fil:
            fil.write(reason)
            fil.write("\n")

    def signal_stop(self, reason):
        """ Notify worker processes and other threads in master to stop by creating the stop signal file"""
        try:
            self.add_reason(reason)
            log_info(f"Added reason to {self.stop_signal_file}.")
        except BaseException as exc:
            message = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format("send stop signal", exc, traceback.format_exc())
            log_error(message)
            raise exc

    def stopping(self):
        """ Return True under one of the below conditions:
                1) the stop signal queue doesn't exist
                2) the stop signal file exists.
            """
        result = os.path.exists(self.stop_signal_file)
        if result:
            self.logger.info("Return stop signal and the caller should exit.")
        return result

    def signal_run(self):
        """ Set the state to non-stopping"""
        if os.path.exists(self.stop_signal_file):
            os.remove(self.stop_signal_file)

    def exit(self, reason):
        """ Exit current process.
        """
        self.logger.info(f"Exit for {reason}.")
        sys.exit(Constant.EXIT_CODE_STOPPED)
