# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""This module provides task representations."""
import json
import os
import pandas as pd
from azure.storage.queue import QueueMessage


class TaskToQueue:
    """Represents a ParallelRunStep task.

    A task can have zero, one or more items. An item can be a file name or a record.
    This is an internal term and should not be exposed to end users.
    End users should take in term of file or record.
    """

    # pylint: disable=redefined-builtin
    def __init__(self, id: int, minibatch: list, location: str = "", message: str = "", partition_size=None):
        """Initialize an instance.

        :param int id:
            The id of the task.
        :param list minibatch:
            A list of items to be processed in the task.
        :param str location:
            For a DataReference, the folder containing the all the files in minibatch.
            For a Dataset, the Dataset name containing all partitions
        """
        self.id = id  # pylint: disable=invalid-name
        self.minibatch = minibatch
        self.location = location.strip()
        self.message = message
        self.partition_size = partition_size

    def to_json(self):
        """Return a json string for the task."""
        return json.dumps(
            {
                "id": self.id,
                "minibatch": self.minibatch,
                "location": self.location,
                "partition_size": self.partition_size,
            }
        )

    @classmethod
    def from_json(cls, json_string):
        """Return a task from a json string."""
        obj = json.loads(json_string)
        result = TaskToQueue(
            id=obj["id"], minibatch=obj["minibatch"], location=obj["location"], partition_size=obj["partition_size"],
        )
        return result


class Task:
    """Represents a ParallelRunStep task to agent, which as dequeue_count.

    A task can have zero, one or more items. An item can be a file name or a record.
    This is an internal term and should not be exposed to end users.
    End users should take in term of file or record.
    """

    # pylint: disable=redefined-builtin
    def __init__(
        self, id: int, dequeue_count: int, minibatch: list, location: str = "", message: str = "", partition_size=None
    ):
        """Initialize an instance.

        :param int id:
            The id of the task.
        :param int dequeue_count:
            The dequeue count of a message. (id, dequeue_count) identifies a round of processing.
        :param list minibatch:
            A list of items to be processed in the task.
        :param str location:
            For a DataReference, the folder containing the all the files in minibatch.
            For a Dataset, the Dataset name containing all partitions
        """
        self.id = id  # pylint: disable=invalid-name
        self.dequeue_count = dequeue_count
        self.minibatch = minibatch
        self.location = location.strip()
        self.message = message
        self.partition_size = partition_size

    def to_json(self):
        """Return a json string for the task."""
        return json.dumps(
            {
                "id": self.id,
                "dequeue_count": self.dequeue_count,
                "minibatch": self.minibatch,
                "location": self.location,
                "partition_size": self.partition_size,
            }
        )

    @classmethod
    def from_json(cls, json_string):
        """Return a task from a json string."""
        obj = json.loads(json_string)
        result = Task(
            id=obj["id"],
            dequeue_count=obj["dequeue_count"],
            minibatch=obj["minibatch"],
            location=obj["location"],
            partition_size=obj["partition_size"],
        )
        return result

    def equals(self, other):
        """Compare the values with the other task."""
        # Not in one concise statement to workaround W503.
        res = self.id == other.id and self.dequeue_count == other.dequeue_count
        res = res and sorted(self.minibatch) == sorted(other.minibatch) and self.location == other.location
        res = res and self.partition_size == other.partition_size
        return res

    def to_pandas_dataframe(self, dataflow, logger) -> pd.DataFrame:
        """ Convert the selected partitions to pandas dataframe.
        """
        logger.debug(f"DatasetLog - Before select_partitions.")
        partition = dataflow.select_partitions(self.minibatch)
        logger.debug(f"DatasetLog - Before to_pandas_dataframe.")
        pdf = partition.to_pandas_dataframe(extended_types=True)
        logger.debug(f"DatasetLog - After to_pandas_dataframe.")
        return pdf

    def get_full_paths(self) -> list:
        """ Get a list of full paths. """
        if self.location == "":
            return self.minibatch

        return [os.path.join(self.location, name) for name in self.minibatch]


class TaskInAzureQueue(Task):
    """Represents a ParallelRunStep task in Azure Storage Queue.

    For one task, there is one message in Azure Storage Queue.
    :ivar :class:`~azure.storage.queue.models.QueueMessage` message:
        reference to the QueueMessage object.
    """

    def __init__(self, message: QueueMessage):
        """Initialize an instance.

        :param azure.storage.queue.models.QueueMessage message:
            A :class:`~azure.storage.queue.models.QueueMessage` object representing the information passed.
        """
        obj = json.loads(message.content)
        super().__init__(
            id=obj["id"],
            dequeue_count=message.dequeue_count,
            minibatch=obj["minibatch"],
            location=obj["location"],
            partition_size=obj["partition_size"],
        )
        self.message = message
