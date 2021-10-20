# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This module privodes a class to resolve the run context."""
from run_context_type import RunContextType
from custom_run_context import CustomRunContext
from aml_compute_run_context import AmlComputueRunContext
from job_args import JobArgs


class RunContextFactory:
    """ The class provides features to resolve the run context.

    The current context type and current context are cached in process as class members.
    """

    MAP = {RunContextType.CUSTOM: CustomRunContext, RunContextType.AML_COMPUTE: AmlComputueRunContext}
    RUN_CONTEXT_TYPE = None
    CURRENT_CONTEXT = None

    @classmethod
    def get_context(cls):
        """ Returns the run context."""
        if cls.CURRENT_CONTEXT is None:
            cls.RUN_CONTEXT_TYPE = JobArgs().run_context_type
            cls.CURRENT_CONTEXT = cls.MAP[cls.RUN_CONTEXT_TYPE]()

        return cls.CURRENT_CONTEXT
