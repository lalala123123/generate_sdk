# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides features to manage local and remote workers on master.
"""
from run_context_factory import RunContextFactory, RunContextType
from logger import get_logger
from custom_node import CustomNode
from masterless_simulator import MasterlessSimulator


class WorkerManager:
    """ The class provides features to manage workers."""

    def __init__(self):
        self.logger = get_logger()
        self.run_context = RunContextFactory.get_context()
        self.custom_node = None
        self.masterless_simulator = None

    def start(self):
        """ Start worker processes on all nodes.
        """
        if RunContextFactory.RUN_CONTEXT_TYPE == RunContextType.CUSTOM:
            if self.custom_node is None:
                self.custom_node = CustomNode()

            self.custom_node.start()

        elif RunContextFactory.RUN_CONTEXT_TYPE == RunContextType.AML_COMPUTE:
            self.logger.info("WorkerManager - Starting workers to process batch task")
            if self.masterless_simulator is None:
                self.masterless_simulator = MasterlessSimulator()

            self.masterless_simulator.start()

        else:
            raise NotImplementedError(f"RunContextType:{RunContextFactory.RUN_CONTEXT_TYPE}")

    def wait(self):
        """ Wait until all processes/threads end."""
        if RunContextFactory.RUN_CONTEXT_TYPE == RunContextType.CUSTOM:
            self.custom_node.wait()

        elif RunContextFactory.RUN_CONTEXT_TYPE == RunContextType.AML_COMPUTE:
            self.logger.info("WorkerManager - Waiting all workers to finished...")
            self.masterless_simulator.wait()
            self.logger.debug("All workers finished.")

        else:
            raise NotImplementedError(f"RunContextType:{RunContextFactory.RUN_CONTEXT_TYPE}")
