# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This is a simulator of AmlCompute to launch Batch inference script on all nodes without the master.

Currently, amlbi_main run the master and then this script will launch worker_main.py on all nodes.

Next step 1:
    After the master election feature is ready, amlbi_main will remove the part to load the master,
    the masterless simulator will main.py on all nodes. main.py will start master and worker process.

Next step 2:
    After AmlCompute is ready to run script on all node, AmlCompute will run main.py all nodes.
    This module will be retired.
"""
import base64
import os
import shlex
import sys

from run_context_factory import RunContextFactory
from shell_exec import ShellExec
from telemetry_logger import log_info


class MasterlessSimulator(ShellExec):
    """ A simulator to launch the script on all nodes.
    """

    def __init__(self):
        super().__init__()
        self.run_context = RunContextFactory.get_context()

    def get_worker_main_cmd(self, single_node=False):
        """ Return the command to run python file"""
        main_file = os.path.join(self.run_context.working_dir, "driver", "worker_main.py")
        self.logger.debug(f"args before encode={' '.join(sys.argv[1:])}")
        b64_args = [base64.b64encode(v.encode("utf-8")).decode("utf-8") for v in sys.argv[1:]]
        script_and_args = f'{shlex.quote(main_file)} {" ".join(b64_args)}'
        if single_node:
            return "python " + script_and_args
        else:
            return script_and_args

    def get_context_manager_wrapped_cmd(self, worker_ip):
        worker_main_cmd = self.get_worker_main_cmd()
        master_node_ip = os.environ.get("AZ_BATCHAI_JOB_MASTER_NODE_IP", "")
        context_manager_wrapped_cmd = "python "
        if worker_ip == master_node_ip:
            # Don't start context managers in master node worker. Will potentially try to mount to an already mounted folder.
            context_manager_wrapped_cmd += f"{worker_main_cmd}"
        else:
            context_manager_file = os.path.join(
                self.run_context.working_dir, "azureml-setup", "context_manager_injector.py"
            )
            context_manager_injection_args = os.environ.get("AZUREML_CONTEXT_MANAGER_INJECTION_ARGS", "")
            context_manager_wrapped_cmd += (
                f"{shlex.quote(context_manager_file)} {context_manager_injection_args} {worker_main_cmd}"
            )
        return context_manager_wrapped_cmd

    def get_ssh_cmd(self, worker_ip):
        """ Get ssh command to start script on a node."""
        path = os.environ.get("PATH")
        if not path:
            raise ValueError('Invalid environment variable "PATH"')

        job_config = os.environ.get("AZ_BATCHAI_JOB_CONFIG", "")

        context_manager_wrapped_cmd = self.get_context_manager_wrapped_cmd(worker_ip)

        hosttools = os.path.join(os.environ.get("AZ_BATCH_NODE_ROOT_DIR", "/mnt/batch/tasks"), "startup/wd/hosttools")

        bash_cmd = (
            f"export AZ_BATCHAI_JOB_CONFIG={job_config};"
            f'export AZ_BATCHAI_TASKLET_CMD="{context_manager_wrapped_cmd}";'
            f"export PATH={shlex.quote(path)};"
            f'export AZ_BATCHAI_WORKER_IP="{worker_ip}";'
            f"cd {shlex.quote(self.run_context.working_dir)};{hosttools} -task=runTaskLet;"
        )

        # Set LogLevel=ERROR to avoid "Added <ip_addr> to known hosts" message for each worker node
        ssh_cmd = f"ssh -o LogLevel=ERROR {shlex.quote(worker_ip)} '{bash_cmd}'"
        self.logger.debug(f"ssh command={ssh_cmd}")
        return ssh_cmd

    def start_ssh_sessions(self, node_ip_list):
        """ Start sessions on all nodes.
        """
        self.logger.info(f"Starting nodes(s) {node_ip_list}.")

        for worker_ip in node_ip_list:
            cmd = self.get_ssh_cmd(worker_ip)
            self.run_async([cmd])

    def start(self):
        """ Start worker on all nodes.
        """
        node_ip_list = self.get_node_ips()
        if node_ip_list:
            # More than one node, use ssh to start workers on all nodes including the master node.
            self.start_ssh_sessions(node_ip_list)
        else:
            # This is only one node, use local shell to start worker.
            log_info(f"Starting worker on single node.")
            cmd = self.get_worker_main_cmd(single_node=True)
            self.run_async([cmd])

    def wait(self):
        """ Wait until all processes/threads end."""
        self.logger.info("Master - Waiting all workers to finished...")

        super().wait()

        self.logger.debug("All threads finished.")

    def get_node_ips(self):
        """ Get the ip addresses of all nodes.
            Return an empty list if running on single node.
        """

        node_list = os.environ.get("AZ_BATCH_NODE_LIST")

        result = []
        if node_list and node_list.strip():
            result = node_list.split(";")

        return result
