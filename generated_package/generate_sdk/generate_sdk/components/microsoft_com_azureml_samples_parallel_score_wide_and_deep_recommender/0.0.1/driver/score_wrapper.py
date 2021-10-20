# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This is a scoring helper module.

This module provides helper classes to call scoring modules provided by users.
"""
import os
import traceback
import pandas

from constant import Message
import utility
from logger import get_logger, get_user_error_logger
from telemetry_logger import log_error
from score_module import ScoreModule
from stop_watch import StopWatch
from progress_status import ProgressStatus
from progress_record import EntryScriptInitRecord, EntryScriptRunRecord
from progress_store import ProgressStore
from entry_script_exception import (
    EntryScriptInitException,
    EntryScriptRunReturnWrongType,
    EntryScriptShutdownException,
)


class ScoreWrapper:
    """ The helper class to load scoring module and call scoring."""

    def __init__(self, module_name):
        self.logger = get_logger()

        self.ip_address = utility.get_ip()

        self.watch = StopWatch()
        self.progress_store = ProgressStore()

        self.scoring_init = None
        self.scoring_shutdown = None
        self.scoring_module = ScoreModule(module_name)
        self.scoring_module.import_module()
        self.scoring_run = self.scoring_module.run

        self.module_name = module_name

    def __reduce__(self):
        return (self.__class__, (self.module_name,))

    def notify_init_progress(self, status):
        """ Notify progress to the master.
        """
        record = EntryScriptInitRecord(
            ip=self.ip_address, pid=os.getpid(), timestamp=self.watch.start_time, status=status
        )
        if status != ProgressStatus.ENTRY_SCRIPT_INIT_START:
            record.elapsed1 = self.watch.elapsed_time
            record.elapsed2 = self.watch.elapsed_process_time

        self.progress_store.notify_progress(record)

    def notify_run_progress(self, task_id, status):
        """ Notify progress to the master.
        """
        record = EntryScriptRunRecord(
            ip=self.ip_address, pid=os.getpid(), timestamp=self.watch.start_time, task_id=task_id, status=status
        )
        if status != ProgressStatus.ENTRY_SCRIPT_RUN_START:
            record.elapsed1 = self.watch.elapsed_time
            record.elapsed2 = self.watch.elapsed_process_time

        self.progress_store.notify_progress(record)

    def notify_shutdown_progress(self, status):
        """ TODO: Track the shutdown event.
            Will add this after we move to azure storage table.
        """

    def init(self):
        """ Call the init() in the entry script one time."""
        if self.scoring_module.init:
            if not self.scoring_init:
                self.scoring_init = self.scoring_module.init

                # TODO: Should we handle the race condition for score init()
                self.logger.debug("Calling init method in scoring module.")
                try:
                    self.watch.reset()
                    self.notify_init_progress(ProgressStatus.ENTRY_SCRIPT_INIT_START)
                    try:
                        self.scoring_init()
                    except BaseException as exc:
                        e_logger = get_user_error_logger()
                        e_logger.error(f"Entry script init() failed for {exc}. Details {traceback.format_exc()}")
                        raise exc

                    self.notify_init_progress(ProgressStatus.ENTRY_SCRIPT_INIT_DONE)
                except BaseException as exc:
                    message = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format(
                        "call scoring init()", exc, traceback.format_exc()
                    )
                    self.logger.error(message)
                    log_error(f"Entry script init() failed {exc}")
                    self.notify_init_progress(ProgressStatus.ENTRY_SCRIPT_INIT_EXCEPTION)
                    raise EntryScriptInitException(message)

                self.logger.debug("init() method in scoring module returned successfully.")

    def run(self, data):
        """ calls the run() method in the score module provided by users."""

        self.init()  # initialize one time if it hasn't.
        try:
            self.logger.debug("Calling run method in scoring module.")
            self.watch.reset()

            if isinstance(data, pandas.DataFrame) and data.empty:
                result = pandas.DataFrame()
            else:
                result = self.scoring_run(data)
            self.logger.debug("Run method in scoring module returned successfully.")

            if isinstance(result, tuple):
                result = list(result)

            if not isinstance(result, list) and not isinstance(result, pandas.DataFrame):
                raise EntryScriptRunReturnWrongType(result)

            return result
        except BaseException as exc:
            e_logger = get_user_error_logger()
            e_logger.error(f"Entry script run() failed for {exc}. Details {traceback.format_exc()}")
            raise exc

    def shutdown(self):
        """ Call the shutdown() in the entry script one time."""
        if self.scoring_module.shutdown:
            if not self.scoring_shutdown:
                self.scoring_shutdown = self.scoring_module.shutdown

                self.logger.debug("Calling shutdown method in scoring module.")
                try:
                    self.watch.reset()
                    self.notify_shutdown_progress(ProgressStatus.ENTRY_SCRIPT_SHUTDOWN_START)
                    try:
                        self.scoring_shutdown()
                    except BaseException as exc:
                        e_logger = get_user_error_logger()
                        e_logger.error(f"Entry script shutdown() failed for {exc}. Details {traceback.format_exc()}")
                        raise exc

                    self.notify_shutdown_progress(ProgressStatus.ENTRY_SCRIPT_SHUTDOWN_DONE)
                except BaseException as exc:
                    message = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format(
                        "call scoring shutdown()", exc, traceback.format_exc()
                    )
                    self.logger.error(message)
                    self.notify_shutdown_progress(ProgressStatus.ENTRY_SCRIPT_SHUTDOWN_EXCEPTION)
                    raise EntryScriptShutdownException(message)

                self.logger.debug("shutdown() method in scoring module returned successfully.")
