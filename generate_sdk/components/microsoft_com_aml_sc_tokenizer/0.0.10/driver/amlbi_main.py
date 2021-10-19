# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This is the Batch Inferencing entry point.

This module should only run on:
    1) Single node AmlCompute.
    2) The master node in a multiple node AmlCompute cluster.

When a job starts, it will:
    1) Initialize a Master instance, which creates three azure storage queues:
        1.1) pending task queue
        1.2) processed task queue
        1.3) signal stop queue - a queue Master sends a signal to stop all worker processes by deleting the queue
    2) Call master.start(), which will start a process to create tasks (enque message),
        polling progress and summarize the result.
    3) master.start() calls worker_manager.start() to:
        3.1) Start worker processes on master node.
        3.2) ssh worker nodes to start worker processes.
    4) Worker processes pick up tasks and run it's run() method on a minibatch
    5) In progress checking in step 2, if all finished or timeout, it will send stop signal.
        All workers will stop after receive stop signal.
    8) Master summarizes the results and reports complete/failed.
    9) Master generates result from temp files for append_row.
"""
import sys
from os import path


def main():
    """ This function:
        1. adds driver folder to sys.path.
        2. start a job.
    """

    # add the folder containing driver scripts to search paths.
    driver_script_folder = path.realpath(path.join(path.abspath(__file__), ".."))
    if driver_script_folder not in sys.path:
        sys.path.insert(0, driver_script_folder)

    from job_starter import JobStarter

    JobStarter().start_job()


if __name__ == "__main__":
    main()
