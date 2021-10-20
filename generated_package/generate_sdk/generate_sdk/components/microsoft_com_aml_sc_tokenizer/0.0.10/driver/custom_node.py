# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides features to start worker on a Windows or Linux machine.
"""
import sys
from pathlib import Path
import shlex
import psutil

from shell_exec import ShellExec


class CustomNode(ShellExec):
    """ This class provides features to start worker on a Windows or Linux machine.
        The node can be Windows or Linux.
    """

    def start(self):
        """ Start the worker in a shell."""
        cmd = self.get_cmd()
        self.run_async(cmd)

    def get_cmd(self):
        """ Return a command to start script locally."""

        # The worker main file is in same path as this file.
        worker_main_file = str(Path(__file__).parents[0] / "worker_main.py")

        if psutil.WINDOWS:
            # worker_main_command = f'python "{worker_main_file}" {" ".join(sys.argv[1:])}'
            worker_main_command = ["python", worker_main_file] + sys.argv[1:]
            self.logger.debug(f"worker_main_command (Windows): {' '.join(worker_main_command)}")
            return worker_main_command

        if psutil.LINUX:
            worker_main_command = [
                " ".join(["python", shlex.quote(worker_main_file)] + [shlex.quote(v) for v in sys.argv[1:]])
            ]
            self.logger.debug(f"worker_main_command (Linux): {' '.join(worker_main_command)}")

            return worker_main_command

        raise NotImplementedError("Not supported platform.")
