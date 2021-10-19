# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides shared features of an AmlCompute node.
"""
import sys
from multiprocessing import current_process

import logger
from run_context_factory import RunContextFactory


class Node:
    """The base class for ParallelRunStep node.

    A *node* represents a single node inside of an AmlCompute Batch Inferencing cluster.
    """

    FIRST_RETRY_INTERVAL = 1

    def __init__(self, args):
        self.args = args
        self.logger = logger.get_logger()

        self.run_context = RunContextFactory.get_context()
        self.run_id = self.run_context.run_id

        if current_process().name == "MainProcess":
            self.logger.debug(f"sys.argv: {sys.argv}")
            self.logger.debug(f"sys.path: {sys.path}")
