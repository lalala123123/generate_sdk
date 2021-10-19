# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
The module provides utilities.
"""
import base64
from datetime import datetime, timedelta
import os
import sys
import zlib

import pandas as pd


def prerequisite_check():
    """
    Check python version
    """
    expected_lowest_version = (3, 5)
    assert (
        sys.version_info >= expected_lowest_version
    ), f"Expected lowest version: {expected_lowest_version}, actual version {sys.version_info}"


def get_ip():
    """ Return the ip address of the current node.

        Don't use socket.gethostbyname(socket.gethostname()) as DNS is not available in some datacenter.
    """
    ip_addr = os.environ.get("AZ_BATCHAI_WORKER_IP", "")
    return ip_addr.strip()


def fmt_time(_timestamp):
    """Convert a timestamp to user readable string."""
    return datetime.fromtimestamp(_timestamp).isoformat()


def timestamp():
    """Return the timestamp of utc now."""
    return datetime.utcnow().timestamp()


def timespan(seconds):
    """Return a string representation of TimeSpan, which can be deserialized in .net service.

    Reference: https://docs.microsoft.com/en-us/dotnet/api/system.timespan.tostring?view=netframework-4.8#System_TimeSpan_ToString
    """
    delta = timedelta(seconds=seconds)
    day = "" if delta.days == 0 else f"{delta.days}."
    hour = delta.seconds // 3600
    minute = (delta.seconds // 60) % 60
    second = delta.seconds % 60

    decimal = ""
    if "." in str(seconds):
        decimal = "." + str(seconds).split(".")[1]

    return f"{day}{hour:02d}:{minute:02d}:{second:02d}{decimal}"


def compress(text: str):
    """ Compress a string and return base64 encoded string. """
    compressed = zlib.compress(bytearray(text, "utf-8"))
    return base64.b64encode(compressed).decode("utf-8")


def decompress(b64_text: str):
    """ Decompress a string generated from b64compress() and return the original one. """
    b64_decoded = base64.b64decode(b64_text)
    return zlib.decompress(b64_decoded).decode("utf-8")


def get_length(values):
    """ Return the length of a pandas DataFrame or a list."""
    if isinstance(values, pd.DataFrame):
        return len(values.index)

    if isinstance(values, list):
        return len(values)

    raise Exception("Only Pandas DataFrame and array of paths allowed as input to scoring module")


def get_available_gpu_count():
    """ Return the number of available GPU."""
    if os.environ.get("AZ_BATCHAI_NUM_GPUS") is not None:
        return int(os.environ["AZ_BATCHAI_NUM_GPUS"])

    return 0
