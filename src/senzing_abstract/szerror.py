#! /usr/bin/env python3

"""
szerror.py manages tranformation from Senzing error number to Python error class.
"""

import datetime
import json
import threading
import traceback
from ctypes import c_char, create_string_buffer, sizeof
from typing import Any, Callable, Dict

from .engine_exception_map import ENGINE_EXCEPTION_MAP, SzError

# Metadata

__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2024-10-03"


# -----------------------------------------------------------------------------
# ErrorBuffer class
# -----------------------------------------------------------------------------


class ErrorBuffer(threading.local):
    """Buffer to call C"""

    # pylint: disable=R0903

    def __init__(self) -> None:
        super().__init__()
        self.string_buffer = create_string_buffer(65535)
        self.string_buffer_size = sizeof(self.string_buffer)


ERROR_BUFFER = ErrorBuffer()
ERROR_BUFFER_TYPE = c_char * 65535


# -----------------------------------------------------------------------------
# Helper functions to create a senzing-specific Exception
# -----------------------------------------------------------------------------


def get_location() -> str:
    """
    Determine caller.

    :meta private:
    """
    stack = traceback.format_stack()
    return stack[0].replace("\n   ", "", 1).rstrip()


def get_message_level(error_id: int) -> str:
    """
    Determine the severity of the error.

    :meta private:
    """
    error_levels = {
        6000: "PANIC",
        5000: "FATAL",
        4000: "ERROR",
        3000: "WARN",
        2000: "INFO",
        1000: "DEBUG",
        0: "TRACE",
    }
    for error_level, error_message in error_levels.items():
        if error_id > error_level:
            return error_message
    return "PANIC"


def get_message_text(error_id: int, id_messages: Dict[int, str], *args: Any) -> str:
    """
    Format the message text from a template and variables.

    :meta private:
    """
    return id_messages.get(error_id, f"No message for index {error_id}.").format(*args)


def get_senzing_error_code(error_text: str) -> int:
    """
    Given an exception string, find the exception code.

    :meta private:
    """
    if len(error_text) == 0:
        return 0
    exception_message_splits = error_text.split("|", 1)
    try:
        result = int(exception_message_splits[0].strip().rstrip("EIW"))
    except ValueError:
        print("ERROR: Could not parse error text '{error_text}'")
        result = 9999
    return result


def get_senzing_error_text(
    get_last_exception: Callable[[ERROR_BUFFER_TYPE, int], str],  # type: ignore
    clear_last_exception: Callable[[], None],
) -> str:
    """
    Get the last exception from the Senzing engine.

    :meta private:
    """
    get_last_exception(
        ERROR_BUFFER.string_buffer,
        sizeof(ERROR_BUFFER.string_buffer),
    )
    clear_last_exception()
    result = ERROR_BUFFER.string_buffer.value.decode()
    return result


def new_szexception(
    get_last_exception: Callable[[ERROR_BUFFER_TYPE, int], str],  # type: ignore
    clear_last_exception: Callable[[], None],
    product_id: str,
    error_id: int,
    id_messages: Dict[int, str],
    *args: Any,
) -> Exception:
    """
    Generate a new Senzing Exception based on the error_id.

    :meta private:
    """
    senzing_error_text = get_senzing_error_text(
        get_last_exception, clear_last_exception
    )
    senzing_error_code = get_senzing_error_code(senzing_error_text)
    message = {
        "time": datetime.datetime.utcnow().isoformat("T"),
        "text": get_message_text(error_id, id_messages, *args),
        "level": get_message_level(error_id),
        "id": f"senzing-{product_id}{error_id:4d}",
        "location": get_location(),
        "errorCode": senzing_error_code,
        "errorText": senzing_error_text,
        "details": args,
    }
    senzing_error_class = ENGINE_EXCEPTION_MAP.get(senzing_error_code, SzError)
    return senzing_error_class(json.dumps(message))
