# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides features to enque and deque progress record.
"""


import json


class ProgressRecord:
    """ Represents the progress record sent from workers to the master."""

    KEYS = []

    def validate(self, **kwargs):
        """Validate if the required properties are in the parameter."""
        for key in self.KEYS:
            if key not in kwargs:
                raise ValueError(f"Missing the property '{key}'.")

    def __init__(self, **kwargs):
        self.validate(**kwargs)

        for key in kwargs:
            setattr(self, key, kwargs[key])

    def to_json(self):
        """ Return the json string representation of this instance."""
        return json.dumps(self.__dict__)

    def match(self, other):
        """ Return True if the other match the identity properties.
        """
        for prop in self.KEYS:
            if getattr(self, prop) != getattr(other, prop):
                return False

        return True

    def __eq__(self, other):
        """ Return True if all properties are same."""
        if not isinstance(other, ProgressRecord):
            return False

        for prop in self.__dict__:
            if getattr(self, prop) != getattr(other, prop):
                return False

        return len(self.__dict__) == len(other.__dict__)

    @classmethod
    def from_json(cls, json_string):
        """ Return a task result from a json string. """
        obj = json.loads(json_string, encoding="utf-8")
        result = ProgressRecord(**obj)
        return result


class EntryScriptInitRecord(ProgressRecord):
    """ Represents the init() progress in the entry script."""

    KEYS = ["ip", "pid", "timestamp"]


class EntryScriptRunRecord(ProgressRecord):
    """ Represents the run() progress in the entry script."""

    KEYS = ["ip", "pid", "timestamp"]
