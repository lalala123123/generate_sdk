# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This is task provider module.
This module provides abstract base class for task providers and concrete provider implemetations.
"""
import abc
import os
import time

from exception import UserInputNotFoundError
from azureml.data._dataset import _Dataset
from azureml._base_sdk_common import _ClientSessionId

import logger
from task import TaskToQueue
from run_context_factory import RunContextFactory


class TaskProvider(abc.ABC):
    """ The abstract base class for task provider. """

    def __init__(self, inputs: list, mini_batch_size: int):
        self.inputs = inputs
        self._total_items = 0
        self.total_tasks = 0
        self.mini_batch_size = mini_batch_size
        self.init_time = time.perf_counter()
        self.init_duration = 0
        self.run_context = RunContextFactory.get_context()
        self.logger = logger.get_logger()

    @property
    def total_items(self):
        """ Return total item count, the total number of files in minibatches
            For TabularDatasetProvider, we want this value to be -1 as it won't know the total item count"""
        if self.__class__ is TabularDatasetProvider:
            return -1
        else:
            return self._total_items

    def init_complete(self):
        """ Update init duration after the first item picked up."""
        self.init_duration = time.perf_counter() - self.init_time

    def create_task(self, minibatch, folder, partition_size=None) -> TaskToQueue:
        """ Count and build a task."""
        self._total_items += len(minibatch)
        task_id, self.total_tasks = self.total_tasks, self.total_tasks + 1  # task id starts from zero
        return TaskToQueue(task_id, minibatch, folder, partition_size=partition_size)

    @abc.abstractmethod
    def get_tasks(self):
        """ Return a generator which yields the list of tasks."""


class FolderOrFileListProvider(TaskProvider):
    """ The class for task provider of a list of folder or file.
        The files in folders won't be in same task as the ones in parameter
         as they could not share the 'path' property in a task.
    """

    def __init__(self, inputs: list, mini_batch_size):
        """
        :param str inputs: This should be Azure BLOB container path (either folder or file).
         Multiple paths or files should be separated by ",".
        """
        super().__init__(inputs, mini_batch_size)
        self.folders = []
        self.init_complete()

    def get_tasks(self):
        """ Return a generator which yields the list of tasks.
            First returns tasks from the files specified in the input parameters.
            Then returns tasks from the files in folders"""

        for task in self.get_tasks_from_files():
            yield task

        for folder in self.folders:
            for task in self.get_tasks_from_folder(folder):
                yield task

    def get_tasks_from_files(self):
        """ Return a generator which yields the list of tasks from the files specified in the input parameters."""
        minibatch = []
        for entry in self.inputs:
            if os.path.isdir(entry):
                self.folders.append(entry)
            else:
                minibatch.append(entry)
                if len(minibatch) == self.mini_batch_size:
                    yield self.create_task(minibatch, "")  # these files don't share a same folder
                    minibatch = []

        if minibatch:  # create a task for remaining items
            yield self.create_task(minibatch, "")  # these files don't share a same folder

    def get_tasks_from_folder(self, folder):
        """ Return a generator which yields the list of tasks from a folder specified in the input parameters"""
        minibatch = []
        for root, _, file_names in os.walk(folder, topdown=True, onerror=None, followlinks=True):
            for file_name in file_names:
                minibatch.append(file_name)
                if len(minibatch) == self.mini_batch_size:
                    yield self.create_task(minibatch, root)
                    minibatch = []

            if minibatch:  # create a task for remaining items at same level
                yield self.create_task(minibatch, root)
                minibatch = []


class FileDatasetProvider(FolderOrFileListProvider):
    """ The class for task provider of a list of FileDatasets"""

    def __init__(self, inputs, mini_batch_size):
        self.logger = logger.get_logger()
        run_context = RunContextFactory.get_context()
        input_datasets = run_context.run.input_datasets
        self.logger.debug(f"inputs: {inputs}, input_datasets: {input_datasets}.")
        if hasattr(input_datasets, "workspace"):
            input_datasets._load_input_datasets()
            input_datasets._initialized = True
            self.logger.debug(f"input_datasets has attribute 'workspace'. input_datasets: {input_datasets}.")

        dataset_paths = []
        for dataset_id in inputs:
            if dataset_id in input_datasets.keys():
                # Some Datasets might have multple paths appended by ';'. Extend add them all to the list.
                dataset_paths.extend(os.path.abspath(input_datasets[dataset_id]).split(";"))

        self.logger.debug(f"input_datasets: {input_datasets}, dataset_paths: {dataset_paths}.")
        super().__init__(dataset_paths, mini_batch_size)


class TabularDatasetProvider(TaskProvider):
    """ The class for task provider of a list of TabularDatasets
    """

    def __init__(self, inputs: list, mini_batch_size: int):
        super().__init__(inputs, mini_batch_size)
        self.workspace = self.run_context.workspace
        self.input_datasets = self.run_context.run.input_datasets
        if hasattr(self.input_datasets, "workspace"):
            self.input_datasets._load_input_datasets()
            self.input_datasets._initialized = True
        if isinstance(inputs, str):
            inputs = [inputs]

        self.inputs = list(set(inputs))
        self.init_complete()

    def get_tasks(self):
        """ Return a generator which yields the list of tasks"""
        self.logger.info(f"DatasetLog - ClientSessionId: {_ClientSessionId}")
        for dataset_id in self.inputs:
            self.logger.debug(f"DatasetLog - Retrieving dataset. id {dataset_id}.")
            if dataset_id in self.input_datasets.keys():
                dataset = self.input_datasets[dataset_id]
            else:
                dataset = _Dataset.get_by_id(self.workspace, dataset_id)
            self.logger.debug("DatasetLog - Retrieved dataset successfully.")
            dataflow = dataset._dataflow
            self.logger.debug("DatasetLog - Retrieved dataflow successfully.")
            dfl = dataflow._with_partition_size(self.mini_batch_size)
            self.logger.debug("DatasetLog - Partition size set successfully.")
            partition_count = self.get_partition_count(dfl, dataset_id)

            self.logger.debug(f"DatasetLog - Retrieved partition count {partition_count}.")
            for i in range(0, partition_count):
                yield self.create_task(
                    [i], dataset_id, partition_size=self.mini_batch_size
                )  # each task has partitions and one dataset_id

    def get_partition_count(self, dataflow, dataset_id):
        """Return the partition count."""
        try:
            return dataflow.get_partition_count()
        except Exception as exc:
            msg = "No files were found using path provided."
            self.logger.exception(f"get tasks for {dataset_id} failed.")
            exc_str = str(exc)
            if msg in exc_str:
                raise UserInputNotFoundError(f"{dataset_id}: {exc_str}")

            raise exc
