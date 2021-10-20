# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The class provides features to report worker progress."""
import csv
from pathlib import Path
import time

from utility import fmt_time, timestamp
from log_config import LogConfig


class WorkerProgressReport:
    """The class provides features to save progress."""

    def __init__(self):
        """Intialize an instance."""
        self.task_csv_writer = None
        self.csv_file = None

    def create_file_once(self):
        """Create the file and add header one time."""
        if self.task_csv_writer is None:
            file_path = Path(LogConfig().get_task_file())
            file_exists = Path(file_path).exists()

            file_path.parent.mkdir(parents=True, exist_ok=True)

            self.csv_file = open(str(file_path), "a", newline="")
            self.task_csv_writer = csv.writer(self.csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if not file_exists:
                self.task_csv_writer.writerow(
                    [
                        "Task Id",
                        "Dequeue Count",
                        "Start Time",
                        "Total",
                        "Succeeded",
                        "Failed",
                        "Elapsed Seconds",
                        "Process Seconds",
                        "Run Method Seconds",
                        "Status",
                        "Error",
                    ]
                )

    def save_progress(self, result):
        """Send progress to file."""
        self.create_file_once()
        self.task_csv_writer.writerow(
            [
                result.id if hasattr(result, "id") else "N/A",
                result.dequeue_count if hasattr(result, "dequeue_count") else "N/A",
                fmt_time(result.start_time if hasattr(result, "start_time") else timestamp()),
                result.total if hasattr(result, "total") else "N/A",
                result.succeeded if hasattr(result, "succeeded") else "N/A",
                (result.total - result.succeeded) if hasattr(result, "total") else "N/A",
                result.duration if hasattr(result, "duration") else "N/A",
                result.process_time if hasattr(result, "process_time") else "N/A",
                result.run_method_time if hasattr(result, "run_method_time") else "N/A",
                str(result.status).replace("ProgressStatus.", ""),
                result.message if hasattr(result, "message") else "",
            ]
        )
        self.csv_file.flush()
