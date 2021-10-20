# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This is Batch Inferencing master entry point.

This module starts to the master to create tasks and track progress.
"""
import sys
from os import path


def main():
    """ This function:
        1. adds driver folder to sys.path.
        2. check prerequisites.
        3. start the master.
    """
    # add the folder containing driver scripts to search paths.
    driver_script_folder = path.realpath(path.join(path.abspath(__file__), ".."))
    if driver_script_folder not in sys.path:
        sys.path.insert(0, driver_script_folder)

    from job_starter import JobStarter

    JobStarter().start_master()


if __name__ == "__main__":
    main()
