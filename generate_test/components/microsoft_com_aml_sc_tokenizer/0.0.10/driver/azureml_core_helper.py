# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides a wrapper of azureml.core related features.
"""
from azureml.core import Experiment, Run

from run_context_factory import RunContextFactory


class AzuremlCoreHelper:
    """ Helper to azureml objects.
    """

    # Status reference: https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.run.run?view=azure-ml
    # -py#get-status-- Per the above doc, get_status() should not return 'Finished'. Actually, for a Completed run,
    # run.status returns 'Completed' and run.get_status() returns 'Finished'
    TERMINAL_STATES = ["Completed", "Failed", "Canceled", "Finished"]

    def __init__(self, workspace=None):
        if workspace is None:
            workspace = RunContextFactory.get_context().workspace

        self.workspace = workspace

    def get_experiments(self):
        """ Return all experiments in current workspace."""
        return Experiment.list(self.workspace)

    def get_runs(self):
        """ Return all child runs of experiments in current workspace.
        """
        for experiment in self.get_experiments():
            for run in Run.list(experiment):
                yield run

    def get_descendant_runs(self, run):
        """ Return a list of all descentdant runs of the specified run."""
        result = []
        for child in run.get_children():
            result.append(child)
            result += self.get_descendant_runs(child)

        return result

    def get_non_terminal_descendant_runs(self):
        """ Return all descendant runs not in terminal state of the child runs of all experiments in the workspace.
            Ignore the child runs of the experiments as they cannot be ParallelRunStep.
        """
        for run in self.get_runs():
            if run.get_status() not in self.TERMINAL_STATES:
                for descendant in self.get_descendant_runs(run):
                    if descendant.get_status() not in self.TERMINAL_STATES:
                        yield descendant
