# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This module defines interface to resolve all external dependencies, including:
        a) azure storage queue, blob
        b) azureml core.

    TODO: Consider removing the environment variable AZ_BATCHAI_INPUT_AZUREML and AZ_BATCHAI_JOB_TEMP
    from this context as they are AmlCompute specific.
"""
from abc import abstractproperty
import os
from pathlib import Path

from singleton_meta import SingletonABCMeta
from logger import get_logger


class RunContext(metaclass=SingletonABCMeta):
    """ Define interface for a run context."""

    def __init__(self):
        super().__init__()
        self.logger = get_logger()
        self._working_dir = None
        self._temp_dir = None

    @abstractproperty
    def run_id(self):
        """ Return the run id.
            Used to globally identify a run instance of a job.
            The master process and all worker processes connect using (workspace, run id).
        """

    @abstractproperty
    def queue_service(self):
        """ Return the queue service that the master to enque into and the workers to deque from.
            In the case of multiple sessions, this needs to be shared among all sessions.
        """

    @abstractproperty
    def workspace(self):
        """ Return the workspace.
            Used in:
            1) queue cleaner
            2) task selection in Task.py (TODO: consider to move this out and also allow to connect other workspace)

            None means the run is not using a workspace.
        """

    @abstractproperty
    def run(self):
        """ Return a run object.
            This is for calling API the from context. The run_id is for correlation. They are not for same purpose.
        """

    @property
    def working_dir(self):
        """ Return the working directory.
            In the case of multiple sessions, this directory needs to be shared among all sessions.
        """
        if self._working_dir is None:
            pth = Path(os.environ.get("AZ_BATCHAI_INPUT_AZUREML", "")).resolve() / self.run_id
            pth.mkdir(parents=True, exist_ok=True)
            self._working_dir = str(pth)

        return self._working_dir

    @property
    def temp_dir(self):
        """ Return a dedicated local temp directory for the current process."""
        if self._temp_dir is None:
            pth = Path(os.environ.get("AZ_BATCHAI_JOB_TEMP", "")).resolve() / "azureml-bi" / str(os.getpid())
            pth.mkdir(parents=True, exist_ok=True)
            self._temp_dir = str(pth)

        return str(self._temp_dir)

    @property
    def experiment_id(self):
        """Return the experiment id of this run."""
