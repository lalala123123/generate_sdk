# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This module provides a stop watch to measure time."""
from datetime import datetime
import time


class StopWatch:
    """ This class implements a stop watch."""

    def __init__(self):
        self.start_time = self.timestamp()
        self.end_time = None

        self.start_process_time = time.process_time()
        self.end_process_time = None

        # If True, don't use current time and use last end_time and end_process_time.
        self.stopped = False

    def timestamp(self):
        """Return the timestamp of utc now."""
        return datetime.timestamp(datetime.utcnow())

    @property
    def elapsed_time(self):
        """ Return elapsed perf counter.
            Keep the current perf counter in end_time.
        """
        self.end_time = self.timestamp()
        return self.end_time - self.start_time

    @property
    def elapsed_process_time(self):
        """ Return elapsed process time.
            Keep the current process time in end_process_time.
        """
        self.end_process_time = time.process_time()
        return self.end_process_time - self.start_process_time

    def reset(self):
        """ Reset start_time and start_process_time to current time."""
        self.start_time = self.timestamp()
        self.end_time = None

        self.start_process_time = time.process_time()
        self.end_process_time = None

        self.stopped = False

    def stop(self):
        """ Record current time as end time"""
        self.end_time = self.timestamp()
        self.end_process_time = time.process_time()
        self.stopped = True

    def __enter__(self):
        self.reset()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
