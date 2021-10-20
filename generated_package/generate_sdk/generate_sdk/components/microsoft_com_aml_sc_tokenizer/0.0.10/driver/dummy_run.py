# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This module provides a dummy simulation of azureml.core.Run.
    This potentially envolves by adding some features based on requirements.
"""
import uuid


class DummyWorkspace:
    """A dummy workspace for running outside of AmlCompute."""


class DummyExperiment:
    """A dummy experiment for running outside of AmlCompute."""

    def __init__(self):
        self.name = "experiment1"
        self.workspace = DummyWorkspace()


class DummyDataset:
    """ A dummy simulation of azureml.core.Run.InputDatasets"""

    items = {}
    workspace = None

    def _load_input_datasets(self):
        """ Do nothing."""

    def __setitem__(self, key, value):
        """ Set item value."""
        DummyDataset.items[key] = value

    def __getitem__(self, key):
        """ Return matched item value."""
        return DummyDataset.items[key]

    def keys(self):
        """ Return keys."""
        return list(DummyDataset.items.keys())


class DummyRun:
    """ A dummy simulation of azureml.core.Run."""

    def __init__(self, depth=0):
        self.id = str(uuid.uuid4())
        self.input_datasets = DummyDataset()
        self.depth = depth
        self.experiment = DummyExperiment()

    def log(self, *args, **kwargs):
        """ Do nothing."""

    def log_row(self, *args, **kwargs):
        """ Do nothing."""

    def add_dataset(self, key, value):
        """Add a mock dataset ininput_datasets"""
        self.input_datasets.__setitem__(key, value)

    @property
    def parent(self):
        """ Return a dummy run."""
        if self.depth == 0:
            return DummyRun(depth=self.depth + 1)

        return None

    def get_details(self):
        """Return a dic contain detail properties."""
        return dict(properties=dict(ComputeTargetType="Custom"))

    def get_status(self):
        """Return the status of the run."""
        return "Completed"
