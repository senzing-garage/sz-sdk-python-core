"""
TODO: g2helpers.py
"""

import os
from typing import Any

SENZING_VERSION_MINIMUM = "4.0.0"
SENZING_VERSION_MAXIMUM = "5.0.0"


def as_normalized_int(candidate_value: Any) -> int:
    """
    Internal processing function.
    This converts many types of values to an integer.

    :meta private:
    """

    if candidate_value is None:  # handle null string
        return int(0)
    if isinstance(candidate_value, str):  # if string is unicode, transcode to utf-8 str
        return int(candidate_value.encode("utf-8"))
    if isinstance(
        candidate_value, bytearray
    ):  # if input is bytearray, assumt utf-8 and convert to str
        return int(candidate_value)
    if isinstance(candidate_value, bytes):
        return int(candidate_value)
    # input is already an int
    return int(candidate_value)


def as_normalized_string(candidate_value: Any) -> Any:
    """
    Internal processing function.

    :meta private:
    """

    if candidate_value is None:  # handle null string
        return b""
    if isinstance(candidate_value, str):  # if string is unicode, transcode to utf-8 str
        return candidate_value.encode("utf-8")
    if isinstance(
        candidate_value, bytearray
    ):  # if input is bytearray, assumt utf-8 and convert to str
        return candidate_value.decode().encode("utf-8")
    if isinstance(candidate_value, bytes):
        return str(candidate_value).encode("utf-8")
    # input is already a str
    return candidate_value


def find_file_in_path(filename: str) -> str:
    """
    Find a file in the PATH environment variable.

    :meta private:
    """
    path_dirs = os.environ["PATH"].split(os.pathsep)
    for path_dir in path_dirs:
        file_path = os.path.join(path_dir, filename)
        if os.path.exists(file_path):
            return file_path
    return ""
