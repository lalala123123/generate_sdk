# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""This module defines run context types.

Keep this in a separate module to avoid cyclic reference.
"""
from enum import IntEnum


class RunContextType(IntEnum):
    """ This class defines the type of the context.
    """

    # Run inside of Aml Compute. Using azureml.core lib to get context.
    AML_COMPUTE = 1

    CUSTOM = 10  # Users to prepare the environment.
