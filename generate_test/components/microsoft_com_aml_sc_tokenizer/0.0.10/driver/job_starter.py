# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides features to start a job, master or worker.
"""
import os
import sys

from job_args import JobArgs
from utility import prerequisite_check, fmt_time, timestamp
from arg_parser import ArgParser
from log_config import LogConfig
from telemetry_logger import log_node_telemetry
from arg_validator import ArgValidator
from job import Job
from master import Master
from worker import Worker


class JobStarter:
    """
    This class provides features to start a job, master or worker.
    """

    def __init__(self):
        """Init counter."""
        self.args = None

        self.start_time = timestamp()

    def setup(self, is_master):
        """ Check and config a job."""

        cwd = os.getcwd()
        if cwd not in sys.path:
            sys.path.insert(0, cwd)

        prerequisite_check()

        args = ArgParser().parse_job_args()
        self.args = JobArgs().from_namespace(args)

        LogConfig().config(args.logging_level, is_master=is_master)
        ArgValidator(args).validate()
        self.args = args

    def start_job(self):
        """ Start a job."""
        self.setup(is_master=True)
        job = Job(self.args)
        job.start()

    def start_master(self):
        """ Start a master."""
        self.setup(is_master=True)
        with Master(self.args) as master:
            master.start()
            master.wait()

    def start_worker(self):
        """ Start a worker."""
        try:
            self.setup(is_master=False)
            worker = Worker(self.args)
            worker.start()
            worker.wait()
        finally:
            now = timestamp()
            log_node_telemetry(
                start_time=self.start_time,
                end_time=now,
                duration=now - self.start_time,
                number_of_cores=os.cpu_count(),
                number_of_nodes=os.environ.get("AZUREML_NODE_COUNT", 1),
                core_seconds=(now - self.start_time) * (os.cpu_count()),
            )
