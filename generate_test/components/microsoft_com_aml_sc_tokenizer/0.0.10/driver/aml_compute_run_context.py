# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This module:
    1. defines job mode.
    2. resolve all external dependencies, including:
        a) azure storage queue, blob
        b) azureml core.
"""
from azure.storage.queue import QueueService
from azureml.core import Run, Experiment

from run_context import RunContext


class AmlComputueRunContext(RunContext):
    """ Resolve the dependencies of the job."""

    def __init__(self):
        super().__init__()
        self._queue_service = None
        self._run = Run.get_context(allow_offline=False)

    @property
    def run_id(self):
        """ Return the run id."""
        return self._run.id

    @property
    def queue_service(self):
        """ Return the queue serivce based on file."""

        if self._queue_service is None:
            datastore = self.workspace.get_default_datastore()
            self._queue_service = QueueService(account_name=datastore.account_name, account_key=datastore.account_key)

        return self._queue_service

    @property
    def run(self):
        """ Return an instance of azureml.core.Run"""
        return self._run

    @property
    def workspace(self):
        """ Return the workspace."""
        return self._run.experiment.workspace

    @property
    def experiment_id(self):
        """Return the experiment id."""
        return Experiment(self._run.experiment.workspace, self._run.experiment.name).id
