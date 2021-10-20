# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides a customized file handler,
which will create parent folders only if there is any log record.
"""
from pathlib import Path
import logging


class CustomFileHandler(logging.handlers.RotatingFileHandler):
    """ This class provides a customized file handler."""

    def __init__(self, filename, mode="a", maxBytes=0, backupCount=0, encoding=None, delay=False):
        self.folder_created = None
        if not delay:
            self.create_folder(filename)

        super().__init__(
            filename=filename, mode=mode, maxBytes=maxBytes, backupCount=backupCount, encoding=encoding, delay=delay
        )

    def create_folder(self, filename):
        """ Try to create the parent folder."""
        Path(filename).resolve().parent.mkdir(parents=True, exist_ok=True)

    def emit(self, record):
        """ For delay=True, try to create the parent folder once."""
        if self.delay and self.folder_created is None:
            self.create_folder(self.baseFilename)
            self.folder_created = True

        super().emit(record)
