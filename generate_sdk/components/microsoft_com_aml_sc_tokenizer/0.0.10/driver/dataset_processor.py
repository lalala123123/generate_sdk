# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides features to process a dataset.
"""
from functools import lru_cache
from azureml.data._dataset import _Dataset
from azureml.dataprep.api.engineapi.engine import use_single_thread_channel

from run_context_factory import RunContextFactory
from task_processor import TaskProcessor

# pylint: disable=protected-access


class DatasetProcessor(TaskProcessor):
    """ A dataset processor."""

    def __init__(self, args):
        super().__init__(args)
        use_single_thread_channel()
        self.input_datasets = self.run_context.run.input_datasets
        if hasattr(self.input_datasets, "workspace"):
            self.input_datasets._load_input_datasets()
            self.input_datasets._initialized = True

    def validate(self, score_output):
        """ Validate output from scoring.run()."""
        raise Exception("Please use TabularDatasetProcessor or FileDatasetListProcessor")

    def get_inputs(self, task):
        """ Get inputs from a task."""
        raise Exception("Please use TabularDatasetProcessor or FileDatasetListProcessor")


class TabularDatasetProcessor(DatasetProcessor):
    """ A tabular dataset processor."""

    def get_inputs(self, task):
        """ Get inputs of the task.
            :param TaskToQueue task, the task to get inputs from.
        """
        self.logger.debug(f"DatasetLog - Before get_inputs. TaskToQueue id {task.id}.")

        dataflow = self.get_dataflow(
            RunContextFactory.get_context().workspace, task.location, task.partition_size, self.logger
        )

        inputs = task.to_pandas_dataframe(dataflow, self.logger)
        self.logger.debug(
            f"DatasetLog - After get_inputs. TaskToQueue id {task.id}. using_tabular_dataset={self.args.using_tabular_dataset}"
        )

        return inputs

    def validate(self, score_output):
        pass

    @lru_cache(maxsize=32)
    def get_dataflow(self, workspace, location, partition_size, logger):
        """ Get dataflow."""
        logger.debug(f"DatasetLog - Retrieving dataset. location {location}.")
        if location in self.input_datasets.keys():
            dataset = self.input_datasets[location]
        else:
            dataset = _Dataset.get_by_id(workspace, location)
        logger.debug("DatasetLog - Retrieved dataset successfully.")
        dataflow = dataset._dataflow
        logger.debug("DatasetLog - Retrieved dataflow successfully.")
        if partition_size:
            dataflow = dataflow._with_partition_size(partition_size)

        return dataflow


class FileDatasetProcessor(TaskProcessor):
    """ A file dataset processor."""

    def get_inputs(self, task):
        """ Get inputs of the task.
            :param TaskToQueue task, the task to get inputs from.
        """

        return task.get_full_paths()

    def validate(self, score_output):
        pass
