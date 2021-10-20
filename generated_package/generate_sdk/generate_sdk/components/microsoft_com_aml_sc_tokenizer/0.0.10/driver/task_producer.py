# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides features to create tasks from a task provider.
"""
import traceback
from pathlib import Path
from threading import Thread

from constant import Constant
from log_config import LogConfig
from event import Event
from telemetry_logger import log_error
from logger import get_logger
from task_manager import TaskManager
from task_provider import FolderOrFileListProvider, TabularDatasetProvider, FileDatasetProvider


class TaskProducer:
    """ The class for task producer.
    """

    def __init__(self, args):
        self.logger = get_logger()

        self.args = args
        self.threads = []
        self.task_manager = TaskManager(args)

        # Set the value to the exceptions so that the caller can know the thread stopped with error.
        self.exceptions = []
        (self.total_tasks, self.total_items) = (0, 0)

        # Trigger when a task created.
        # With parameters:
        # (sender, task_id)
        self.on_task_created = Event()

        # Trigger when all task created
        # With parameters:
        # (sender)
        self.on_all_tasks_created = Event()

        self.task_manager.on_task_created += self.task_manager_on_task_created

    def task_manager_on_task_created(self, sender, task_id):
        """ Event handler for task_manager.on_task_created().
            Trigger the event on_task_created of this object.
        """
        self.on_task_created(sender, task_id)

    def get_task_provider(self):
        """ Get a task provider per the input type."""
        if self.args.using_tabular_dataset:
            task_provider = TabularDatasetProvider(self.args.input_tabular_datasets, self.args.mini_batch_size)
        elif self.args.using_file_dataset:
            task_provider = FileDatasetProvider(self.args.input_file_datasets, self.args.mini_batch_size)
        else:
            task_provider = FolderOrFileListProvider(self.args.inputs, self.args.mini_batch_size)

        return task_provider

    def _create_tasks(self):
        """ Read tasks from the task provider and call the task manager to create tasks."""
        try:
            task_provider = self.get_task_provider()

            self.task_manager.create_tasks(task_provider)

            self.total_tasks, self.total_items = (task_provider.total_tasks, task_provider.total_items)
            self.on_all_tasks_created(self)

        except BaseException as exc:
            self.exceptions.append(exc)
            error = (
                f"Exception occurred while scheduling {Constant.TERM_MINI_BATCHES}: {exc}.\n{traceback.format_exc()}"
            )
            log_error(error)
            raise exc

    def get_profile_filename(self):
        """Return the filename for profile output."""
        log_dir = LogConfig().log_dir
        profile_dir = Path(log_dir) / "sys"
        profile_dir.mkdir(parents=True, exist_ok=True)
        return str(profile_dir / "master.task_producer.profile")

    def create_tasks(self):
        """If profiling_module specified, call _create_tasks() with profile.
            Or call _create_tasks() directly.
        """
        module = self.args.profiling_module
        if module:
            from profile_wrapper import ProfileWrapper

            ProfileWrapper(module).runctx(
                "self._create_tasks()", globals(), locals(), filename=self.get_profile_filename()
            )
        else:
            self._create_tasks()

    def start(self):
        """ Start a process to create tasks and update completed summary."""
        thr = Thread(target=self.create_tasks, args=())
        thr.start()
        self.threads.append(thr)
        self.logger.info(f"Task creation started in a separate thread with name {thr.name} and id {thr.ident}")

    def force_stop_task_creation(self):
        """ Force to stop task creatation"""
        self.task_manager.force_stop_task_creation()
        self.wait()

    def wait(self):
        """ Wait the thread to end."""

        for thr in self.threads:
            thr.join()

        self.logger.debug("Thread finished.")

        self.logger.info("TaskPRoducer - Batch tasks created")
