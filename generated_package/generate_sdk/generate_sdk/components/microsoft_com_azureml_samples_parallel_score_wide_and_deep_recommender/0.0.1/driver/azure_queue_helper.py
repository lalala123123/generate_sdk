# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides azure storage queue related features.
"""
import hashlib
from uuid import UUID
import logger
import utility
from run_context_factory import RunContextFactory


class AzureQueueHelper:
    """The helper class for azure storage queue operations.

    An *azurequeuehelper* represents an azure storage queue helper.

    .. remarks::

        A azurequeuehelper is an object used to provide an azure storage queue operations.

        Functionality includes:

        *  Create/delete a queue.
        *  Send messages to a queue.
        *  Get messages from a queue.
        *  Delete messages from a queue.
        *  List all queues.
        *  Get message count in the queue.

        Reference:
        https://docs.microsoft.com/en-us/azure/storage/queues/storage-python-how-to-use-queue-storage
        https://docs.microsoft.com/en-us/python/api/azure-storage-queue/azure.storage.queue.queueservice.queueservice?view=azure-python
    """

    # A single queue message can be up to 64 KB in size.
    # https://docs.microsoft.com/en-us/azure/storage/queues/storage-python-how-to-use-queue-storage
    MESSAGE_SIZE_LIMIT_IN_BYTE = 64 * 1024

    def __init__(self, queue_name):
        self.logger = logger.get_logger()
        self.run_context = RunContextFactory.get_context()

        self.queue_name = queue_name
        self.queue_service = self.run_context.queue_service

    @classmethod
    def name_from_run_id(cls, run_id: str):
        """Map the run id to be a valid part of a queue name.

        If the run id is an UUID, just return the run id.
        Otherwise, return a str if hex digest of sha224. The length is 56.
        Choose sha224 as the length of the queue name must be less than 63.
        The digest is expected to be unique accross all run ids and must be same for a run id across all nodes.
        """
        try:
            UUID(run_id)
            return run_id
        except ValueError:
            return hashlib.sha224(bytes(run_id, "utf-8")).hexdigest()

    def put_message(self, message):
        """ Enque the message."""
        message = utility.compress(message)
        assert (
            len(message.encode("utf-8")) < self.MESSAGE_SIZE_LIMIT_IN_BYTE
        ), "A single queue message can be up to 64 KB in size"
        self.queue_service.put_message(self.queue_name, message)

    def get_messages(self, num_messages=1, visibility_timeout=30):
        """ Deque a message."""
        messages = self.queue_service.get_messages(
            self.queue_name, num_messages=num_messages, visibility_timeout=visibility_timeout
        )
        for message in messages:
            message.content = utility.decompress(message.content)
        return messages

    def delete_message(self, message):
        """ Delete a message from the queue.
        """
        self.queue_service.delete_message(self.queue_name, message.id, message.pop_receipt)

    def clear_messages(self, timeout=None):
        """ Deletes all messages from the queue.
        """
        self.queue_service.clear_messages(self.queue_name, timeout)

    def update_message_visibility_timeout(self, message, visibility_timeout: int):
        """
        Updates the visibility timeout of a message.
        This operation can be used to continually extend the invisibility of a queue message.
        This functionality can be useful if you want a worker role to "lease" a queue message.
        For example, if a worker role calls get_messages and recognizes that it needs more time to process a message,
        it can continually extend the message's invisibility until it is processed.
        If the worker role were to fail during processing, eventually the message would become visible again
         and another worker role could process it.

        Reference:
        https://docs.microsoft.com/en-us/python/api/azure-storage-queue/azure.storage.queue.queueservice.queueservice?view=azure-python#update-message-queue-name--message-id--pop-receipt--visibility-timeout--content-none--timeout-none-
        """
        new_message = self.queue_service.update_message(
            self.queue_name, message.id, message.pop_receipt, visibility_timeout
        )
        message.pop_receipt = new_message.pop_receipt
        message.time_next_visible = new_message.time_next_visible

    def create_queue(self):
        """ Create the queue."""
        result = self.queue_service.create_queue(self.queue_name)
        if not result:
            self.logger.debug("Queue already exists. Continue.")
        return result

    def delete_queue(self):
        """ Delete the queue.
        """
        self._delete_queue(self.queue_name)

    def get_approximate_message_count(self):
        """ Return approximate message count in the queue.
        """
        return self._get_approximate_message_count(self.queue_name)

    def list_queues(self):
        """ Return a list of all queues in current account.
        """
        return self.queue_service.list_queues()

    def delete_queues(self, queue_names):
        """ Delete the queues"""
        for queue_name in queue_names:
            self._delete_queue(queue_name)

    # private methods
    def _delete_queue(self, queue_name):
        """ Delete the queue.
        """
        if not self.queue_service.exists(queue_name):
            self.logger.warning(f"Queue not found for queue {queue_name}. Unable to delete.")
            return

        message_count = self._get_approximate_message_count(queue_name)
        if message_count > 0:
            self.logger.warning(f"Deleting non-empty queue {queue_name} with {message_count} message(s).")

        self.logger.debug(f"Deleting queue {queue_name} starts.")
        self.queue_service.delete_queue(queue_name)
        self.logger.debug(f"Deleting queue {queue_name} ends")

    def _get_approximate_message_count(self, queue_name):
        """ Return approximate message count in the queue.
        """
        metadata = self.queue_service.get_queue_metadata(queue_name)
        return metadata.approximate_message_count

    def exists(self, timeout=None):
        """ Return True if the queue exists."""
        return self.queue_service.exists(self.queue_name, timeout)
