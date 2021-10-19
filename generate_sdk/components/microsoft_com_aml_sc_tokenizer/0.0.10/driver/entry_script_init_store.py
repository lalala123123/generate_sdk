# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This module defines features to track the statuses of the entry script,
    by implementing a store EntryScriptInitRecord.
"""
from logger import get_logger
from progress_status import ProgressStatus


class EntryScriptInitStore(dict):
    """ Track statuses of all runs of the entry script.
        The types of the statuses are defined in the module progress_status.
    """

    def __init__(self):
        self.logger = get_logger()

        super().__init__()
        self.add_methods = {
            ProgressStatus.ENTRY_SCRIPT_INIT_START: self.add_start,
            ProgressStatus.ENTRY_SCRIPT_INIT_EXCEPTION: self.add_exception,
            ProgressStatus.ENTRY_SCRIPT_INIT_TIMEOUT: self.add_timeout,
            ProgressStatus.ENTRY_SCRIPT_INIT_DONE: self.add_done,
        }

    def get_key(self, record):
        """ Get the key from a record"""
        return record.ip, record.pid, record.timestamp

    def add(self, record):
        """ Add a progress record to the store."""
        if record.status not in [
            ProgressStatus.ENTRY_SCRIPT_INIT_START,
            ProgressStatus.ENTRY_SCRIPT_INIT_EXCEPTION,
            ProgressStatus.ENTRY_SCRIPT_INIT_TIMEOUT,
            ProgressStatus.ENTRY_SCRIPT_INIT_DONE,
        ]:
            raise ValueError(f"The record {record.to_json()} has un-supported status {record.status}.")

        self.logger.debug(f"Add {record.to_json()}.")
        self.add_methods[record.status](record)

    def validate_pair(self, key):
        """ Validate and raise ValueError if there is no record to pair with."""
        if key not in self:
            # Don't enforce the rule as it may not deque in order.
            # raise ValueError(f"Could not find the an existing record for the key {key}.")
            self.logger.debug(f"Could not find the an existing record for the key {key}.")

    def add_start(self, record):
        """ Add a record with status ENTRY_SCRIPT_INIT_START."""
        key = self.get_key(record)
        if key not in self:  # Avoid override result, in rare case, the records may not be in order.
            self[key] = record

    def add_exception(self, record):
        """ Add a record with status ENTRY_SCRIPT_INIT_EXCEPTION."""
        key = self.get_key(record)
        self.validate_pair(key)

        if key not in self:
            self[key] = record
        else:
            if self[key].status == ProgressStatus.ENTRY_SCRIPT_INIT_START:
                self[key] = record

    def add_timeout(self, record):
        """ Add a record with status ENTRY_SCRIPT_INIT_TIMEOUT."""
        key = self.get_key(record)
        self.validate_pair(key)

        if key not in self:
            self[key] = record
        else:
            if self[key].status == ProgressStatus.ENTRY_SCRIPT_INIT_START:
                self[key] = record

    def add_done(self, record):
        """ Add a record with status ENTRY_SCRIPT_INIT_DONE."""
        key = self.get_key(record)
        self.validate_pair(key)
        self[key] = record

    def count_by_status(self):
        """ Count the items in the store by status.
            Return a dict with statuses as key and count as value.
        """
        res = {
            ProgressStatus.ENTRY_SCRIPT_INIT_START: 0,
            ProgressStatus.ENTRY_SCRIPT_INIT_EXCEPTION: 0,
            ProgressStatus.ENTRY_SCRIPT_INIT_TIMEOUT: 0,
            ProgressStatus.ENTRY_SCRIPT_INIT_DONE: 0,
        }
        for value in self.values():
            res[value.status] += 1

        return res
