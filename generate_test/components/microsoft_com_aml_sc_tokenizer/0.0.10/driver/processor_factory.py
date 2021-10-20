# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides features to get a task processor.
"""
from dataset_processor import TabularDatasetProcessor, FileDatasetProcessor
from list_processor import ListProcessor


class ProcessorFactory:
    """ Return task processor based on the input type."""

    def __init__(self, args):
        self.args = args

    def get_processor(self):
        """ Return a processor."""

        if self.args.using_tabular_dataset:
            processor = TabularDatasetProcessor(self.args)
        elif self.args.using_file_dataset:
            processor = FileDatasetProcessor(self.args)
        else:
            processor = ListProcessor(self.args)

        return processor
