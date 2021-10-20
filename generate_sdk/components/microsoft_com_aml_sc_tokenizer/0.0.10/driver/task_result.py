# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides task result representation.
"""
import json

# pylint: disable=redefined-builtin, invalid-name
class TaskResult:
    """ Represents processing result of a ParallelRunStep task.
        A task result is identified by (task id, ip, pid, start_time).
        Start_time is the timestamp when the task being picked. Keep the value not changed for one round process.
    """

    def __init__(
        self,
        id: int,  # task id
        dequeue_count: int,
        total: int,
        succeeded: int,
        failed: int,
        ip: str,
        pid: int,  # ip address, process id
        start_time: int,
        duration: int,
        process_time: int,
        run_method_time: int,
        status: int,  # Defined in progress_status
    ):
        """
        :param int id:
            The id of the task.
        :param int total:
            Total number of the items of the task.
        :param int succeeded:
            Succeeded number of the items.
        :param int failed:
            Failed number of the items.
        """
        self.id = id
        self.dequeue_count = dequeue_count
        self.total = total
        self.succeeded = succeeded
        self.failed = failed
        self.ip = ip
        self.pid = pid
        self.start_time = start_time
        self.duration = duration
        self.process_time = process_time
        self.run_method_time = run_method_time
        self.status = status

    def to_json(self):
        """ Return a json representation of this object."""
        return json.dumps(
            {
                "id": self.id,
                "dequeue_count": self.dequeue_count,
                "total": self.total,
                "succeeded": self.succeeded,
                "failed": self.failed,
                "ip": self.ip,
                "pid": self.pid,
                "start_time": self.start_time,
                "duration": self.duration,
                "process_time": self.process_time,
                "run_method_time": self.run_method_time,
                "status": self.status,
            }
        )

    def to_array(self):
        """ Return an array representation of this object."""
        return [
            self.id,
            self.dequeue_count,
            self.total,
            self.succeeded,
            self.failed,
            self.ip,
            self.pid,
            self.start_time,
            self.duration,
            self.process_time,
            self.run_method_time,
            self.status,
        ]

    def match(self, other):
        """ Return True if the other match the identity properties.
        """
        props = ["id", "ip", "pid", "start_time"]

        for prop in props:
            if getattr(self, prop) != getattr(other, prop):
                return False

        return True

    @classmethod
    def from_json(cls, json_string):
        """ Return a task result from a json string. """
        obj = json.loads(json_string, encoding="utf-8")
        result = TaskResult(
            id=obj["id"],
            dequeue_count=obj["dequeue_count"],
            total=obj["total"],
            succeeded=obj["succeeded"],
            failed=obj["failed"],
            ip=obj["ip"],
            pid=obj["pid"],
            start_time=obj["start_time"],
            duration=obj["duration"],
            process_time=obj["process_time"],
            run_method_time=obj["run_method_time"],
            status=obj["status"],
        )
        return result
