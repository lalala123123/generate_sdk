# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This module provides features of poisoned tasks.
    A task will be deleted and put into poisoned tasks if cannot be processed after retry 3 times.
    The cause may be:
    1. Processing failed with exception.
    2. Processing doesn't finish within the allowed timeout and the task being picked by other worker processes.
        The total pick up times exceeds 3.
"""
import os
from datetime import datetime
import glob

import utility
from log_config import LogConfig
import logger
from progress_store import ProgressStore
from progress_status import ProgressStatus
from task import TaskInAzureQueue
from task_result import TaskResult


class PoisonTask:
    """ Manage poisoned tasks."""

    def __init__(self):
        self.logger = logger.get_logger()
        self.log_dir = os.path.join(LogConfig().log_dir, "sys")
        os.makedirs(self.log_dir, exist_ok=True)
        ip_address = utility.get_ip()
        pid = os.getpid()
        self.poison_task_file = os.path.join(self.log_dir, f"poison_tasks_{ip_address}_{pid}.txt")

        self.pattern = os.path.join(self.log_dir, "poison_task*.txt")

    def exists(self):
        """ True if there is any poisoned tasks."""
        files = glob.glob(self.pattern)
        return len(files) > 0

    def add(self, message):
        """ Add a task to the poison file.
        """
        # notify progress so that the job can stop for poisoned task.
        task = TaskInAzureQueue(message)
        task_result = TaskResult(
            id=task.id,
            dequeue_count=task.dequeue_count,
            total=len(task.minibatch),
            succeeded=0,
            failed=len(task.minibatch),
            ip=utility.get_ip(),
            pid=os.getpid(),
            start_time=datetime.utcnow().timestamp(),
            duration=0,
            process_time=0,
            run_method_time=0,
            status=ProgressStatus.TASK_POISONED,
        )

        self.logger.debug(f"Notify poisoned task {task_result}")
        store = ProgressStore()
        store.notify_progress(task_result)

        with open(self.poison_task_file, "a") as fil:
            fil.write(message.content)
            if not message.content.endswith("\n"):
                fil.write("\n")
