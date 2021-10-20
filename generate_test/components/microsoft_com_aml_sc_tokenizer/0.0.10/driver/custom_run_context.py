# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This module provides a run context in a single session."""
from unittest.mock import Mock

from dummy_run import DummyRun
from run_context import RunContext
from local_file_queue import LocalFileQueueService
from job_args import JobArgs


class CustomRunContext(RunContext):
    """ Resolve the dependencies of the job."""

    def __init__(self):
        super().__init__()

        self._run = DummyRun()
        self._run_id = None
        self._workspace = None

    @property
    def run_id(self):
        """ Return the run id."""

        if self._run_id is None:
            self._run_id = JobArgs().run_id

        return self._run_id

    @run_id.setter
    def run_id(self, value):
        """ Set the run id."""
        self._run_id = value

    @property
    def run(self):
        return self._run

    @property
    def queue_service(self):
        """ Return the queue serivce based on file."""
        return LocalFileQueueService()

    @property
    def workspace(self):
        """ Return the workspace."""
        if self._workspace is None:
            self._workspace = Mock()

        return self._workspace

    @property
    def experiment_id(self):
        """Return a dummy experiment id."""
        return "dummy_experiment_id"
