# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This is Batch Inferencing worker entry point.

This module starts to process tasks.
"""
import base64
import sys
import os
from os import path


def main():
    """ This function:
        1. adds driver folder to sys.path.
        2. check prerequisites.
        3. start worker processes.
    """
    # add the folder containing driver scripts to search paths.
    driver_script_folder = path.realpath(path.join(path.abspath(__file__), ".."))
    if driver_script_folder not in sys.path:
        sys.path.insert(0, driver_script_folder)

    if "AZUREML_RUN_ID" in os.environ:  # This is in AmlCompute. Decode the args.
        sys.argv = sys.argv[:1] + [base64.b64decode(v).decode("utf-8") for v in sys.argv[1:]]

    from job_starter import JobStarter

    JobStarter().start_worker()


if __name__ == "__main__":
    main()
