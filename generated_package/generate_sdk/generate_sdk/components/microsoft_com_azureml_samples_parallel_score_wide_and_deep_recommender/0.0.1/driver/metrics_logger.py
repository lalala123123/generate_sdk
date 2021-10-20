# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides metrics logging functionality.
"""

from run_context_factory import RunContextFactory


class MetricsLogger:
    """ This class provides metrics logging functionality."""

    def __init__(self, metrics_name_prefix="", push_metrics_to_parent=False):
        self.run = RunContextFactory.get_context().run
        self.metrics_name_prefix = metrics_name_prefix
        self.push_metrics_to_parent = push_metrics_to_parent

    def log(self, name, value):
        """ Add metric to run context with given metrics_name_prefix+name as name and value.
            If called with same name again portal will show it as graph.
            If push_metrics_to_parent is set to true then the same metric is pushed to parent run.
            :param name, metric name.
            :param value, metric value - integer only since we ignore 0 and negative values
        """
        self.run.log(self.metrics_name_prefix + name, value)
        if self.push_metrics_to_parent:
            self.run.parent.log(self.metrics_name_prefix + name, value)

    def log_processing_status(self, processed_task_count, processed_item_count):
        """ Log processing status."""
        self._log_status("Processing Status", processed_task_count, processed_item_count)

    def log_remaining_status(self, remaining_task_count, remaining_item_count):
        """ In case of tabular dataset remaining item count is not known in that case
            just log remaining mini batches.
        """
        if self._should_log(remaining_task_count):
            self.log("Remaining Mini Batches", remaining_task_count)
            if remaining_item_count >= 0:
                self.log("Remaining Items", remaining_item_count)

    def _log_status(self, metric_name, task_count, item_count):
        if self._should_log(task_count):
            self.run.log_row(self.metrics_name_prefix + metric_name, MiniBatches=task_count, Items=item_count)
            if self.push_metrics_to_parent:
                self.run.parent.log_row(
                    self.metrics_name_prefix + metric_name, MiniBatches=task_count, Items=item_count
                )

    def _should_log(self, number):
        """ To reduce metric footprint in run context, log first (processing) / last (remaining)
            1000 entries, after that every 5th entry till 5000 and then every 1000th entry.
        """
        should_log = False
        if number < 1000 or (number < 5000 and number % 5 == 0) or number % 1000 == 0:
            should_log = True

        return should_log
