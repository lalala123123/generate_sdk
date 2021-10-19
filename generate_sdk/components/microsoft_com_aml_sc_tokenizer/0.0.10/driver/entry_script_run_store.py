# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This module defines features to track the issues of the run() method in entry script,
    by implementing a store EntryScriptRunRecord.
    Tracking issues only to reduce resource usages.
"""
from logger import get_logger
from progress_status import ProgressStatus


class EntryScriptRunStore(dict):
    """ Track statuses of some run error of the entry script.
        The types of the statuses are defined in the module progress_status.
    """

    def __init__(self):
        self.logger = get_logger()

        super().__init__()
        self.add_methods = {
            ProgressStatus.ENTRY_SCRIPT_RUN_START: self.add_start,
            ProgressStatus.ENTRY_SCRIPT_RUN_EXCEPTION: self.add_exception,
            ProgressStatus.ENTRY_SCRIPT_RUN_TIMEOUT: self.add_timeout,
            ProgressStatus.ENTRY_SCRIPT_RUN_DONE: self.add_done,
        }

    def get_key(self, record):
        """ Get the key from a record"""
        return record.ip, record.pid, record.timestamp, record.task_id

    def add(self, record):
        """ Add a progress record to the store."""
        if record.status not in [
            ProgressStatus.ENTRY_SCRIPT_RUN_START,
            ProgressStatus.ENTRY_SCRIPT_RUN_EXCEPTION,
            ProgressStatus.ENTRY_SCRIPT_RUN_TIMEOUT,
            ProgressStatus.ENTRY_SCRIPT_RUN_DONE,
        ]:
            raise ValueError(f"The record {record.to_json()} has un-supported status {record.status}.")

        self.logger.debug(f"Add {record.to_json()}.")
        self.add_methods[record.status](record)

    def add_start(self, record):
        """ Add a record with status ENTRY_SCRIPT_RUN_START."""
        key = self.get_key(record)
        if key not in self:  # Avoid override result, in rare case, the records may not be in order.
            self[key] = record

    def add_exception(self, record):
        """ Add a record with status ENTRY_SCRIPT_RUN_EXCEPTION."""
        key = self.get_key(record)

        if key not in self:
            self[key] = record
        else:
            if self[key].status == ProgressStatus.ENTRY_SCRIPT_RUN_START:
                self[key] = record

    def add_timeout(self, record):
        """ Add a record with status ENTRY_SCRIPT_RUN_TIMEOUT."""
        key = self.get_key(record)

        if key not in self:
            self[key] = record
        else:
            if self[key].status == ProgressStatus.ENTRY_SCRIPT_RUN_START:
                self[key] = record

    def add_done(self, record):
        """ Add a record with status ENTRY_SCRIPT_RUN_DONE."""
        key = self.get_key(record)
        self[key] = record

    def count_by_status(self):
        """ Count the items in the store by status.
            Return a dict with statuses as key and count as value.
        """
        res = {
            ProgressStatus.ENTRY_SCRIPT_RUN_START: 0,
            ProgressStatus.ENTRY_SCRIPT_RUN_EXCEPTION: 0,
            ProgressStatus.ENTRY_SCRIPT_RUN_TIMEOUT: 0,
            ProgressStatus.ENTRY_SCRIPT_RUN_DONE: 0,
        }
        for value in self.values():
            res[value.status] += 1

        return res
