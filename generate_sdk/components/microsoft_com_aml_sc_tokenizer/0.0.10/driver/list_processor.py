# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides features to process a list.
"""
from task_processor import TaskProcessor


class ListProcessor(TaskProcessor):
    """ A list processor."""

    def get_inputs(self, task):
        """ Get inputs of the task.
            :param Task task, the task to get inputs from.
        """

        return task.get_full_paths()

    def validate(self, score_output):
        pass
