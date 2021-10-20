# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
    Simulate only the features of QueueService that Batch Inferencing are using.
    Don't simulate other features.
"""
import os
from pathlib import Path
import shutil
import uuid
from datetime import datetime
from types import SimpleNamespace

from filelock import FileLock

# pylint: disable=unused-argument


class LocalFileQueueService:
    """
        Simulate only the features of QueueService that Batch Inferencing are using.
        Don't simulate other features.
    """

    # keep the root dir as sibling of this script and use an absolute path.
    # As working dir will be changed in sub processes, a relative path doesn't work.
    DRIVER_DIR = Path(__file__).parent
    QUEUE_ROOT_DIR = str(DRIVER_DIR / ".local_file_queue")
    LOCK_FILE = str(DRIVER_DIR / "queue.lock")
    DATA_FILE = "data.txt"
    DEFAULT_VISIBILITY_TIMEOUT = 30

    def __init__(
        self,
        account_name=None,
        account_key=None,
        sas_token=None,
        is_emulated=False,
        protocol="https",
        endpoint_suffix="core.windows.net",
        request_session=None,
        connection_string=None,
        socket_timeout=None,
        token_credential=None,
    ):  # pylint: disable=too-many-arguments
        # Allow multiple processes to initialize concurrently.
        os.makedirs(self.QUEUE_ROOT_DIR, exist_ok=True)

        self.account_name = account_name
        self.account_key = account_name

    def _log(self, message):
        pass

    def _get_queue_path(self, queue_name):
        return os.path.join(self.QUEUE_ROOT_DIR, queue_name)

    def _get_data_file(self, queue_name):
        return os.path.join(self._get_queue_path(queue_name), self.DATA_FILE)

    def _load_data(self, queue_name):
        """ Return a list of all messages
        """
        self._log(f"_load_data:{os.getcwd()}")
        from_row = lambda r: SimpleNamespace(
            id=r[0], content=r[1], time_next_visible=float(r[2]), pop_receipt=r[3], dequeue_count=int(r[4])
        )
        with open(self._get_data_file(queue_name), "r") as data_file:
            rows = []
            for line in data_file:
                if line.strip() != "":
                    rows.append(from_row(line.strip().split(",")))
            return rows

    def _save_data(self, queue_name, data):
        with open(self._get_data_file(queue_name), "w", encoding="utf-8", newline="") as data_file:
            for msg in data:
                data_file.write(
                    f"{msg.id},{msg.content},{msg.time_next_visible},{msg.pop_receipt},{msg.dequeue_count}\n"
                )
            self._log(f"{data}")

    def create_queue(self, queue_name, metadata=None, fail_on_exist=False, timeout=None):
        """ Create a queue."""
        with FileLock(self.LOCK_FILE):
            queue_path = self._get_queue_path(queue_name)

            if os.path.exists(queue_path):
                return False

            os.makedirs(queue_path)

            self._log(f"{queue_name}")
            self._save_data(queue_name, [])
            return True

    def delete_message(
        self, queue_name, id, pop_receipt, timeout=None
    ):  # pylint: disable=invalid-name,redefined-builtin
        """ Delete a message."""
        with FileLock(self.LOCK_FILE):
            messages = self._load_data(queue_name)
            for index, message in enumerate(messages):
                if message.id == id:
                    del messages[index]

                    self._save_data(queue_name, messages)
                    break

    def delete_queue(self, queue_name, fail_not_exist=False, timeout=None):
        """ Delete a queue."""
        with FileLock(self.LOCK_FILE):
            self._log(queue_name)
            shutil.rmtree(self._get_queue_path(queue_name))

    def exists(self, queue_name, timeout=None):
        """ Return True if queue exists."""
        with FileLock(self.LOCK_FILE):
            self._log(queue_name)
            return os.path.exists(self._get_queue_path(queue_name))

    def get_messages(self, queue_name, num_messages=None, visibility_timeout=None, timeout=None):
        """ Get messages."""
        with FileLock(self.LOCK_FILE):
            now_timestamp = datetime.timestamp(datetime.utcnow())
            messages = self._load_data(queue_name)
            for message in messages:
                if message.time_next_visible <= now_timestamp:
                    if visibility_timeout is None:
                        message.time_next_visible = (
                            now_timestamp + self.DEFAULT_VISIBILITY_TIMEOUT
                        )  # defaults to 30 seconds
                    else:
                        message.time_next_visible = now_timestamp + visibility_timeout

                    message.dequeue_count += 1

                    self._save_data(queue_name, messages)
                    return [message]

            return []

    def get_queue_metadata(self, queue_name, timeout=None):
        """ Get metadata of a queue."""
        with FileLock(self.LOCK_FILE):
            return SimpleNamespace(approximate_message_count=len(self._load_data(queue_name)))

    def list_queues(
        self, prefix=None, num_results=None, include_metadata=False, marker=None, timeout=None
    ):  # pylint: disable=too-many-arguments
        """ List queues."""
        with FileLock(self.LOCK_FILE):
            return [SimpleNamespace(name=name) for name in os.listdir(self.QUEUE_ROOT_DIR)]

    def put_message(
        self, queue_name, content, visibility_timeout=None, time_to_live=None, timeout=None
    ):  # pylint: disable=too-many-arguments
        """ Enque a message."""
        with FileLock(self.LOCK_FILE):
            if visibility_timeout is None:
                time_next_visible = datetime.timestamp(datetime.utcnow())
            else:
                time_next_visible = datetime.timestamp(datetime.utcnow()) + visibility_timeout

            message = SimpleNamespace(
                id=f"{uuid.uuid4()}",
                content=content,
                time_next_visible=time_next_visible,
                pop_receipt=f"{uuid.uuid4()}",
                dequeue_count=0,
            )

            messages = self._load_data(queue_name)
            messages.append(message)
            self._save_data(queue_name, messages)

    def update_message(
        self, queue_name, id, pop_receipt, visibility_timeout, content=None, timeout=None
    ):  # pylint: disable=invalid-name,redefined-builtin
        """ Update a message in the queue."""
        with FileLock(self.LOCK_FILE):
            now_timestamp = datetime.timestamp(datetime.utcnow())
            messages = self._load_data(queue_name)
            for message in messages:
                if message.id == id:
                    message.time_next_visible = now_timestamp + visibility_timeout
                    message.pop_receipt = f"{uuid.uuid4()}"
                    self._save_data(queue_name, messages)
                    return message

    def clear_messages(self, queue_name, timeout=None):
        """ Deletes all messages from the specified queue.
        """
        with FileLock(self.LOCK_FILE):
            self._save_data(queue_name, [])
