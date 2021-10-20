# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" The module provides features to parse command-line arguments.
    Users can provide more arguments which are not used in the driver.
    The driver will keeps all arguments so that users can use them in the entry script.
"""
import argparse
import math
import os
import re

from constant import Constant
from run_context_type import RunContextType


class ArgParser:
    """ The class parses command line arguments."""

    def __init__(self):
        self.args = None

    def _parse_inputs(self, unknown_args, input_prefix):
        """ Return a list of Azure BLOB container paths (either folder or file).
            Duplicates will be removed.
        """
        inputs = []
        remain_args = []
        value_index = -1
        for index, arg in enumerate(unknown_args):
            if index == value_index:
                continue
            arg_name = rf"^{input_prefix}\d+$"
            if re.match(arg_name, arg, re.M | re.I):
                value_index = index + 1
                assert value_index <= len(unknown_args), f"missing value for parameter {arg}"
                inputs.append(unknown_args[value_index])
            else:
                arg_name = rf"^{input_prefix}\d+=(.+)$"
                match = re.match(arg_name, arg, re.M | re.I)
                if match:
                    pth = match.groups()[0]
                    if pth not in inputs:
                        inputs.append(pth)
                else:
                    remain_args.append(arg)

        return inputs, remain_args

    def _strip(self, text):
        """ Remove the quotes from a text so that it can be converted to number."""
        if text and isinstance(text, str):
            return text.strip("\"'").strip()

        return text

    def _get_error_threshold(self, text):
        """ Return error threshold from a string."""
        text = self._strip(text)
        try:
            val = int(text)
        except ValueError:
            try:
                # convert float to int as we allowed users to pass in percentage in float before.
                val = math.ceil(float(text))
            except ValueError:
                val = -1

        if val < -1:
            val = -1

        return val

    def add_common_args(self, parser):
        """Add common args."""
        # *** basic parameters start ***
        parser.add_argument(
            "--inputs",
            required=False,
            # Mark '--inputs' as optional and then assign later from input*.
            # This is to work around the issue that AmlCompute won't expand a list of DataReference.
            default=[],
            type=list,
            help="This is a placeholder, which will be assigned from a list of Azure BLOB container path (either "
            'folder or file) specified in parameters like "--input1=path1 --input2=path2 ...".\n'
            "AmlCompute cannot expand a list of DataReferences, so we need to pass one by one as a workaround.",
        )
        parser.add_argument(
            "--output",
            required=False,
            default=None,
            type=str,
            help="This should be AML Pipelines output class: PipelineData",
        )
        parser.add_argument(
            "--output_action", type=str.lower, choices=["summary_only", "file", "append_row"], required=True
        )
        parser.add_argument(
            "--append_row_file_name",
            type=str.lower,
            default=Constant.DEFAULT_APPEND_ROW_FILE_NAME,
            required=False,
            help="The name of the output file if output_action is 'append_row'",
        )
        parser.add_argument(
            "--scoring_module_name",
            required=True,
            help="The score module name. If passing in a file path, file name without file type will be used.",
        )
        parser.add_argument(
            "--mini_batch_size", type=int, required=False, default=1, help="The mini batch size for your run() method"
        )
        parser.add_argument("--logging_level", required=False, default="INFO", help="The logging level.")
        parser.add_argument("--input_format", type=str.lower, required=False, help="Keep for backwards compatibilty")

        # *** basic parameters end ***

        # *** advance parameters start ***
        parser.add_argument(
            "--resource_monitor_interval",
            type=int,
            required=False,
            default=30,
            help=f"The interval to monitor system and process resource usage.",
        )
        parser.add_argument(
            "--nice",
            type=int,
            required=False,
            default=5,
            help="The 'niceness' of all the processes in the job."
            " Only works on Linux and will be ignored on other platforms."
            " The higher the nice value, the lower the priority of all the processes. The range is [0, 20]."
            " If the value is lower than the current niceness, it will be ignored.",
        )
        parser.add_argument(
            "--metrics_name_prefix",
            type=str,
            required=False,
            default="",
            help="Prefix to be used for all metrics to be added to run history.",
        )
        parser.add_argument(
            "--push_metrics_to_parent",
            type=str,
            required=False,
            default="False",
            help="Flag to indicate if run history metrics "
            "should be pushed to parent run along with current (step) run.",
        )
        # *** advance parameters end ***
        parser.add_argument("--run_id", required=False, type=str, help="The identity of a run.")
        parser.add_argument(
            "--run_context_type",
            required=False,
            type=int,
            choices=[RunContextType.CUSTOM, RunContextType.AML_COMPUTE],
            default=RunContextType.AML_COMPUTE,
            help="The type of this run context.",
        )
        parser.add_argument(
            "--profiling_module",
            type=str,
            default="",
            choices=["", "cProfile", "profile"],
            required=False,
            help="The profiler used to generate profile. Default to '', which doesn't do profiling."
            "The generated profile file will be saved in logs/sys/",
        )
        parser.add_argument(
            "--client_sdk_version",
            type=str,
            default="",
            required=False,
            help="Client SDK version used to create ParallelRunStep.",
        )

    def add_master_args(self, parser):
        """Add master specific args."""
        parser.add_argument(
            "--error_threshold",
            type=str,
            required=False,
            default="-1",
            help="The number of failures which can be ignored so that processing should continue.\n"
            "The job checks progress every second. If the number of failed records exceeds this value, "
            "the job will be stopped and reported as failed.\n"
            "E.g. If user provides a folder containing 1000 images and sets the error threshold to 50 then "
            f"ParallelRunStep will ignore 50 failures, but will stop if more than 50 {Constant.TERM_ITEMS} failed.\n"
            "Set to -1 to ignore all failed {Constant.TERM_ITEMS}.",
        )
        parser.add_argument(
            "--progress_update_timeout",
            type=int,
            required=False,
            default=-1,
            help="If there is progress update, the job will timeout.",
        )
        parser.add_argument(
            "--cleanup_leaked_queues",
            type=str,
            required=False,
            default="1",
            help='Set "1" or "true" to have a process to cleanup leaked queues.',
        )
        parser.add_argument(
            "--first_task_creation_timeout",
            type=int,
            required=False,
            default=600,
            help=f"The max waiting time (in seconds) for scheduling the first {Constant.TERM_MINI_BATCH}."
            " For dataprep api, it may take 10+ seconds to several minutes in the worst case to initialize.",
        )

    def add_worker_args(self, parser):
        """Add worker specific args."""
        parser.add_argument(
            "--run_invocation_timeout",
            "--score_run_timeout",
            type=int,
            required=False,
            default=60,
            help="The max duration that the run method allows to take. If it exceeds this setting, "
            f"the {Constant.TERM_MINI_BATCH} will be reassigned to other workers",
        )
        parser.add_argument(
            "--task_overhead_timeout",
            type=int,
            required=False,
            default=30,
            help=f"The max overhead of initialization of a {Constant.TERM_MINI_BATCH}.",
        )
        parser.add_argument(
            "--process_count_per_node",
            required=False,
            default=os.cpu_count(),
            help="Number of processes to start on each node.",
        )

    def parse(self, parser, args):
        """Parse based on the argument definition and return the result."""
        args, unknown_args = parser.parse_known_args(args)
        args.inputs, unknown_args = self._parse_inputs(unknown_args, "--input")
        args.input_tabular_datasets, unknown_args = self._parse_inputs(unknown_args, "--input_ds_")
        args.using_tabular_dataset = len(args.input_tabular_datasets) != 0
        args.input_file_datasets, unknown_args = self._parse_inputs(unknown_args, "--input_fds_")
        args.using_file_dataset = len(args.input_file_datasets) != 0
        args.unknown = unknown_args
        return args

    def parse_job_args(self, args=None):
        """ Parse all arguments and assign to self.args."""
        parser = argparse.ArgumentParser(allow_abbrev=False, description="ParallelRunStep Worker")
        self.add_common_args(parser)
        self.add_master_args(parser)
        self.add_worker_args(parser)

        args = self.parse(parser, args)

        self.normalize_common_args(args)
        self.normalize_master_args(args)
        self.normalize_worker_args(args)

        self.args = args
        return args

    def parse_worker_args(self, args=None):
        """ Parse all arguments and assign to self.args."""
        parser = argparse.ArgumentParser(allow_abbrev=False, description="ParallelRunStep Worker")
        self.add_common_args(parser)
        self.add_worker_args(parser)

        args = self.parse(parser, args)

        assert args.run_id, "Missing run_id for worker."

        self.normalize_common_args(args)
        self.normalize_worker_args(args)

        self.args = args
        return args

    def normalize_common_args(self, args):
        """ Normalize the common args returned from argparse."""
        if args.output_action not in ["summary_only", "file", "append_row"]:
            raise NotImplementedError(f"output_action:{args.output_action}")

        if args.push_metrics_to_parent.lower() in ("yes", "true", "1"):
            args.push_metrics_to_parent = True
        else:
            args.push_metrics_to_parent = False

        # Convert values to number/bool as PythonScriptStep adds quote to all values
        if args.mini_batch_size:
            args.mini_batch_size = int(self._strip(args.mini_batch_size))

        args.scoring_module_name = self.get_module_name(args.scoring_module_name)

        if args.nice < 0:
            args.nice = 0

        if args.output is not None:
            os.environ["AZUREML_BI_OUTPUT_PATH"] = args.output  # This may be used in score.py.

    def normalize_master_args(self, args):
        """ Normalize the master specific args returned from argparse."""
        if args.progress_update_timeout:
            args.progress_update_timeout = int(self._strip(args.progress_update_timeout))
            if args.progress_update_timeout < 0:
                args.progress_update_timeout = 3 * (args.run_invocation_timeout + args.task_overhead_timeout)

        args.error_threshold = self._get_error_threshold(args.error_threshold)

        args.cleanup_leaked_queues = self._strip(args.cleanup_leaked_queues).lower() in ["true", "1"]

    def normalize_worker_args(self, args):
        """ Normalize the worker specific args returned from argparse."""
        if args.process_count_per_node:
            args.process_count_per_node = int(self._strip(args.process_count_per_node))

        if not args.process_count_per_node or args.process_count_per_node < 1:
            args.process_count_per_node = os.cpu_count()

    def get_module_name(self, scoring_module_name):
        """ Get module name from a file name."""
        if scoring_module_name.strip() == "":
            raise ValueError(
                "The parameter scoring_module_name can not be empty string or whitespace. "
                "Please provide a valid value. "
            )
        if scoring_module_name.endswith(".py"):
            scoring_module_name = scoring_module_name[:-3]

        return scoring_module_name.replace("/", ".").replace("\\", ".")
