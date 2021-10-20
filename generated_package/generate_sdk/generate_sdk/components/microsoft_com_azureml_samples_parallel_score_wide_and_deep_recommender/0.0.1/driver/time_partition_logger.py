# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""This module provides features to log partitioned by time.

Logs will be always appended in azureml portal, the old rows will still be there after rotation.
As a result, the built-in rotating file handler doesn't work.
"""
import os
from datetime import datetime
from pathlib import Path
import queue
import traceback

from singleton_meta import SingletonMeta
from log_config import LogConfig


class TimePartitionLogger(metaclass=SingletonMeta):
    """The class provides a timed partition logger."""

    def __init__(self):
        """Init the log folder and the queue to accept messages."""
        self.log_dir = LogConfig().get_log_dir()
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)

        self.que = queue.Queue()
        self.pattern = "%Y-%m-%d"  #  Partition by date

    def get_file(self):
        """Get the file name."""
        utcnow = datetime.utcnow()
        time_partition = utcnow.strftime(self.pattern)
        base_name = f"overview.{time_partition}.txt"
        full_name = Path(self.log_dir) / base_name
        return full_name

    def put(self, msg):
        """Put a message to the queue.

        This method is thread-safe.
        """
        self.que.put((datetime.utcnow(), msg))

    def flush(self, msg=None):
        """Flush messages in queue.

        This method is not thread-safe.
        """
        if msg:
            self.put(msg)

        try:
            with open(self.get_file(), "a", newline=os.linesep) as fil:
                try:
                    while True:
                        entry = self.que.get_nowait()
                        fil.write(f"{entry[0].isoformat()} {entry[1]}\n")
                except queue.Empty:
                    pass

        except BaseException as exc:  # pylint: disable=broad-except
            # Swallow logging error, print to 70_driver.txt and continue.
            print(
                f"{datetime.utcnow()} TimePartitionLogger.flush() failed with error {exc}."
                f" Detail {traceback.format_exc()}."
            )
