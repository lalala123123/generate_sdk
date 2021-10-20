# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module defines progress status.
"""

from enum import IntEnum


class ProgressStatus(IntEnum):
    """ This class defines the status of the progress.
        Worker processes report the status to the master.
    """

    # Entry script
    ENTRY_SCRIPT_INIT_START = 11  # The before calling init()
    ENTRY_SCRIPT_INIT_EXCEPTION = 12  # The init() method raises exception
    ENTRY_SCRIPT_INIT_TIMEOUT = 13  # The init() method timeout
    ENTRY_SCRIPT_INIT_DONE = 14  # The init() done

    ENTRY_SCRIPT_RUN_START = 21  # The before calling run()
    ENTRY_SCRIPT_RUN_EXCEPTION = 22  # The run() method raises exception
    ENTRY_SCRIPT_RUN_TIMEOUT = 23  # The run() method timeout
    ENTRY_SCRIPT_RUN_DONE = 24  # The run() done

    # Entry script
    ENTRY_SCRIPT_SHUTDOWN_START = 31  # The before calling shutdown()
    ENTRY_SCRIPT_SHUTDOWN_EXCEPTION = 32  # The shutdown() method raises exception
    ENTRY_SCRIPT_SHUTDOWN_TIMEOUT = 33  # The shutdown() method timeout
    ENTRY_SCRIPT_SHUTDOWN_DONE = 34  # The shutdown() done

    # Status of a task
    TASK_PICKED = 50
    TASK_POISONED = 51  # A task was poisoned on the fourth pick up.
    TASK_PROCESS_TIMEOUT = 60  # Including run() timeout
    TASK_PROCESSED = 99
