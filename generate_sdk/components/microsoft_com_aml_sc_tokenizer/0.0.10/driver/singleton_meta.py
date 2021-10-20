# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""This module provides a singleton metaclass.

Class using this as metaclass will be in singleton pattern.
"""
from abc import ABCMeta


class SingletonMeta(type):
    """This is a singleton metaclass."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonABCMeta(ABCMeta, SingletonMeta):
    """This is a singleton ABC metaclass."""
