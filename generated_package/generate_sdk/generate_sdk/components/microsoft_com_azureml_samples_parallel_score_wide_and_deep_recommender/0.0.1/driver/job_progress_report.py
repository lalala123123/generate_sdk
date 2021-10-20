# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides reports of the job progress.
"""

import csv
from datetime import datetime
import os

from progress_status import ProgressStatus
import logger
from log_config import LogConfig


class JobProgressReport:
    """ This class provides features to generate reports of a progress store."""

    def __init__(self, progress_store):
        self.logger = logger.get_logger()
        self.log_dir = LogConfig().log_dir
        self.progress_store = progress_store

        self.processed_tasks = progress_store.processed_tasks
        self.processed_saved_index = -1

        self.pending_tasks = progress_store.pending_tasks
        self.override_tasks = progress_store.override_tasks

        self.dir = os.path.join(self.log_dir, "sys/report")
        os.makedirs(self.dir, exist_ok=True)

        self.processed_result_file = os.path.join(self.dir, "processed_tasks.csv")
        self.pending_result_file = os.path.join(self.dir, "pending_tasks.csv")
        self.override_result_file = os.path.join(self.dir, "override_tasks.csv")

        self.pending_header = ["Task Id", "Ip Address", "Process Id", "Start Time"]

        self.processed_header = self.pending_header + [
            "Total",
            "Succeeded",
            "Failed",
            "Elapsed Seconds",
            "Process Seconds",
            "Run Method Seconds",
        ]

    def format(self, task_result):
        """ Format a task result into a readable row."""
        tsk = task_result
        start_time = datetime.fromtimestamp(tsk.start_time).isoformat()
        result = [tsk.id, tsk.ip, tsk.pid, start_time]
        if tsk.status == ProgressStatus.TASK_PROCESSED:
            result += [tsk.total, tsk.succeeded, tsk.failed, tsk.duration, tsk.process_time, tsk.run_method_time]

        return result

    def save_pending(self):
        """ Save pending tasks to a csv file before job stops.
            If there is no such task, it won't generate this report.
            The job should fail if there is any pending task.
        """
        self.progress_store.remove_processed()
        results = []
        for task_list in self.pending_tasks.values():
            results += task_list

        if results:
            with open(self.pending_result_file, "w", newline="") as result_file:
                writer = csv.writer(result_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(self.pending_header)
                for task_result in results:
                    writer.writerow(self.format(task_result))

    def save_processed(self):
        """ Save processed tasks to a csv file.
            A completed job should always have this report.
        """
        if self.processed_saved_index < len(self.processed_tasks) - 1:
            with open(self.processed_result_file, "a", newline="") as result_file:
                writer = csv.writer(result_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                if self.processed_saved_index < 0:
                    writer.writerow(self.processed_header)
                for task_result in list(self.processed_tasks.values())[self.processed_saved_index + 1 :]:
                    writer.writerow(self.format(task_result))
                self.processed_saved_index = len(self.processed_tasks) - 1

    def save_override(self):
        """ Save tasks being override to a csv file.
            If there is no such task, it won't generate the report.
        """
        results = []
        for task_list in self.override_tasks.values():
            results += task_list

        if results:
            with open(self.override_result_file, "w", newline="") as result_file:
                writer = csv.writer(result_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                header = [f"Prior {t}" for t in self.processed_header] + self.processed_header
                writer.writerow(header)
                for task_result in results:
                    writer.writerow(self.format(task_result) + self.format(task_result.by))

    def save(self):
        """ Save all task results to files on the master node.
        """
        self.save_override()
        self.save_pending()
