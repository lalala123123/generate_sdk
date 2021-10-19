# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""This module provides features to manage arguments of a job.

TODO: Add validation here using ArgParser as reference.
"""
import os

from constant import Constant
from run_context_type import RunContextType
from singleton_meta import SingletonMeta


class CommonArgs(metaclass=SingletonMeta):
    """Common arguments for master and worker."""

    # Arguments from users.
    ARG_NAMES = {
        "inputs",
        "input_tabular_datasets",
        "using_tabular_dataset",
        "input_file_datasets",
        "using_file_dataset",
        "output",
        "output_action",
        "append_row_file_name",
        "scoring_module_name",
        "mini_batch_size",
        "logging_level",
        "input_format",
        "resource_monitor_interval",
        "nice",
        "metrics_name_prefix",
        "push_metrics_to_parent",
        "run_context_type",
        "run_id",
        "profiling_module",
        "client_sdk_version",
        "unknown",  # Keep the unknown_args to pass to entry script via sys.argv.
    }

    RESERVED_MEMBERS = ["arg_names"]

    def __init__(self, **kwargs):
        self.arg_names = self.ARG_NAMES

        self.set_args(**kwargs)

    def __setattr__(self, name, value):
        """ Ensure the attribute is in the known list."""

        if name not in self.RESERVED_MEMBERS:
            if name not in self.arg_names:
                raise ValueError(f"Invalid attribute name: '{name}'.")

        super().__setattr__(name, value)

    def command_line_args(self):
        """Return an list of command line args."""
        result = []
        for name in self.arg_names:
            if name == "inputs":
                result.extend([f"--input{index}={value}" for index, value in enumerate(getattr(self, name))])
            elif name == "input_tabular_datasets":
                result.extend([f"--input_ds_{index}={value}" for index, value in enumerate(getattr(self, name))])
            elif name == "input_file_datasets":
                result.extend([f"--input_fds_{index}={value}" for index, value in enumerate(getattr(self, name))])
            elif name == "unknown":
                result.extend(getattr(self, "unknown"))
            else:
                result.append(f"--{name}={getattr(self, name)}")

        return result

    def from_namespace(self, namespace):
        """Return an instance from an argparse namespace."""
        for name in self.arg_names:
            setattr(self, name, getattr(namespace, name))

        return self

    def set_args(self, **kwargs):
        """Change to the passing in values."""
        for key, value in kwargs.items():
            setattr(self, key, value)


class MasterArgs(CommonArgs):
    """Master arguments."""

    ARG_NAMES = {"error_threshold", "progress_update_timeout", "cleanup_leaked_queues", "first_task_creation_timeout"}

    def __init__(self, **kwargs):
        super().__init__()
        self.arg_names = super().ARG_NAMES.union(self.ARG_NAMES)

        self.set_args(**kwargs)


class WorkerArgs(CommonArgs):
    """Worker arguments."""

    ARG_NAMES = {"run_invocation_timeout", "task_overhead_timeout", "process_count_per_node"}

    def __init__(self, **kwargs):
        super().__init__()
        self.arg_names = super().ARG_NAMES.union(self.ARG_NAMES)

        self.set_args(**kwargs)


class JobArgs(CommonArgs):  # pylint: disable=too-many-instance-attributes
    """This class manages arguments of a job."""

    def __init__(self, **kwargs):
        super().__init__()
        self.arg_names = CommonArgs.ARG_NAMES.union(MasterArgs.ARG_NAMES).union(WorkerArgs.ARG_NAMES)

        # Required arguments
        self.inputs = []
        self.input_tabular_datasets = []
        self.using_tabular_dataset = False
        self.input_file_datasets = []
        self.using_file_dataset = False
        self.output = ""
        self.scoring_module_name = ""

        # Optional
        self.mini_batch_size = 1
        self.logging_level = "INFO"
        self.input_format = None
        self.output_action = "summary_only"
        self.append_row_file_name = Constant.DEFAULT_APPEND_ROW_FILE_NAME
        self.error_threshold = -1
        self.run_invocation_timeout = 60
        self.task_overhead_timeout = 30
        self.resource_monitor_interval = 30
        self.process_count_per_node = os.cpu_count()
        self.progress_update_timeout = 270
        self.cleanup_leaked_queues = True
        self.nice = 5
        self.first_task_creation_timeout = 600
        self.metrics_name_prefix = ""
        self.push_metrics_to_parent = False
        self.run_id = None
        self.run_context_type = RunContextType.AML_COMPUTE
        self.profiling_module = ""
        self.client_sdk_version = ""

        self.unknown = []

        self.set_args(**kwargs)

    @property
    def worker_args(self):
        """Return args for workers, which is a subset of job args."""
        args = WorkerArgs()
        for name in args.arg_names:
            setattr(args, name, getattr(self, name))
        return args
