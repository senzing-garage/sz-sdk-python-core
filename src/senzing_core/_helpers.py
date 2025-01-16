"""
TODO: _helpers.py
"""

# NOTE This is to prevent TypeError: '_ctypes.PyCPointerType' object is not subscriptable
# on _Pointer[c_char]) for FreeCResources
# ctypes._Pointer is generic for type checkers, but at runtime it's not generic, so annotations
# import is necessary - or string annotation ("_Pointer[c_char]") .
from __future__ import annotations

import json
import os
import sys
import threading
from contextlib import suppress
from ctypes import (
    CDLL,
    POINTER,
    ArgumentError,
    _Pointer,
    c_char,
    c_char_p,
    c_uint,
    cast,
    cdll,
    create_string_buffer,
    sizeof,
)
from ctypes.util import find_library
from functools import wraps
from types import TracebackType
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

from senzing import ENGINE_EXCEPTION_MAP, SzError

# TODO
# if sys.version_info < (3, 10):
if sys.version_info < (3, 11):
    from typing_extensions import ParamSpec, Self
else:
    from typing import ParamSpec, Self

T = TypeVar("T")
P = ParamSpec("P")

START_DSRC_JSON = '{"DATA_SOURCES": ['
START_ENTITIES_JSON = '{"ENTITIES": ['
START_RECORDS_JSON = '{"RECORDS": ['
END_JSON = "]}"

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------


class FreeCResources:
    """
    Free C resources when calling engine APIs

    :meta private:
    """

    def __init__(self, handle: CDLL, resource: _Pointer[c_char]) -> None:
        self.handle = handle
        self.resource = resource

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.handle.SzHelper_free(self.resource)


# -----------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------


def catch_non_sz_exceptions(func_to_decorate: Callable[P, T]) -> Callable[P, T]:
    """
    The Python SDK methods convert Python types to ctypes and utilize helper functions. If incorrect types/values are
    used standard library exceptions are raised not SzError exceptions as the Senzing library hasn't been called
    yet. Raise the original Python exception type and append information to identify the SDK method called, accepted
    arguments & types and the arguments and types the SDK method received. Also convert ctypes.ArgumentError exceptions
    to TypeError, a user shouldn't need to import ctypes to catch ArgumentError

    :meta private:
    """

    @wraps(func_to_decorate)
    def wrapped_func(*args: P.args, **kwargs: P.kwargs) -> T:  # pylint: disable=too-many-locals
        try:
            return func_to_decorate(*args, **kwargs)
        except (ArgumentError, TypeError, ValueError, json.JSONDecodeError) as err:
            append_err_msg = ""

            # Remove the Senzing engine object from args
            received_arg_values = list(args[1:])

            # Append a custom message if received arguments are likely incorrect type, value, etc. If any positional
            # arguments are missing don't append to the original error message
            missing_positional = bool(err.args and " required positional argument" in err.args[0])
            if (received_arg_values or kwargs) and not missing_positional:
                # Get wrapped function annotation, remove unwanted keys
                annotations_dict = func_to_decorate.__annotations__
                with suppress(KeyError):
                    del annotations_dict["return"]
                    del annotations_dict["kwargs"]

                # Get the wrapped functions argument names and determine which, if any, positional args were received
                # and capture the signature names and received values
                func_signature_names = list(annotations_dict.keys())
                received_arg_names = func_signature_names[: len(received_arg_values)]
                received_args = {received_arg_names[a]: received_arg_values[a] for a in range(len(received_arg_names))}

                # Add names and values of any key word arguments and order on the wrapped function signature
                all_received = {**received_args, **kwargs}
                all_received_ordered = {k: all_received[k] for k in annotations_dict if k in all_received}

                # Get the wrapped function signature names and types and build a string for append to the error message
                func_signature = ", ".join(
                    [
                        f"{name}: {type if isinstance(type, str) else type.__name__}"
                        for name, type in annotations_dict.items()
                    ]
                )

                # TODO: Figure out why these lines prevent the error in the ".join(..) command":
                # UnboundLocalError: cannot access local variable 'type' where it is not associated with a value
                # See https://docs.python.org/3.12/whatsnew/changelog.html#id28 gh-118513
                # See https://github.com/python/cpython/issues/118513

                join_list = []
                for name, value in all_received_ordered.items():
                    join_list.append(f"{name}: {type(value).__name__}")
                func_received = ", ".join(join_list)

                # Get the wrapped functions received argument names and types
                # func_received = ", ".join(
                #     [f"{name}: {type(value).__name__}" for name, value in all_received_ordered.items()]
                # )

                # print(f"\n{all_received_ordered = }", flush=True)
                # Get the wrapped functions received argument names and types
                # func_received = ", ".join(
                #     [f"{name}: {type(value).__name__}" for name, value in all_received_ordered.items()]
                # )
                # TODO
                # print(f"\n{func_received = }", flush=True)

                append_err_msg = f" - [Called: {func_to_decorate.__module__}.{func_to_decorate.__name__}({func_signature}) - Received: {func_received}]"

            err_args = err.args
            arg_0 = append_err_msg if not err_args else f"{err_args[0]}{append_err_msg}"
            err.args = (arg_0,) + err_args[1:]

            if err.__class__.__name__ == "ArgumentError":
                raise TypeError(err) from err
            raise err

    return wrapped_func


# -----------------------------------------------------------------------------
# Helpers for loading Senzing C library
# -----------------------------------------------------------------------------
def load_sz_library(lib: str = "") -> CDLL:
    """
    Check the OS name and load the appropriate Senzing library.

    :meta private:
    """
    try:
        if os.name == "nt":
            win_path = find_library(lib if lib else "Sz")
            return cdll.LoadLibrary(win_path if win_path else "")

        return cdll.LoadLibrary(lib if lib else "libSz.so")
    except OSError as err:
        # TODO Wording & links for V4
        print(
            f"ERROR: Unable to load the Senzing library: {err}\n"
            "ERROR: Did you remember to setup your environment by sourcing the setupEnv file?\n"
            "ERROR: For more information: https://senzing.zendesk.com/hc/en-us/articles/115002408867-Introduction-G2-Quickstart\n"
            "ERROR: If you are running Ubuntu or Debian also review the ssl and crypto information at https://senzing.zendesk.com/hc/en-us/articles/115010259947-System-Requirements",
        )
        raise sdk_exception(1) from err


# -----------------------------------------------------------------------------
# Helpers for checking and handling results from C library calls
# -----------------------------------------------------------------------------


def check_result_rc(
    lib_get_last_exception: Callable[[_Pointer[c_char], int], str],
    lib_clear_last_exception: Callable[[], None],
    lib_get_last_exception_code: Callable[[], int],
    result_return_code: int,
) -> None:
    """
    Check the return code from calling the C API, raise an error if not 0.

    :meta private:
    """
    if result_return_code != 0:
        raise engine_exception(
            lib_get_last_exception,
            lib_clear_last_exception,
            lib_get_last_exception_code,
        )


# -----------------------------------------------------------------------------
# Helpers for building JSON strings for Senzing engine APIs
# -----------------------------------------------------------------------------


# TODO - Investigate adding and recalling is working correctly
def escape_json_str(to_escape: str) -> str:
    """
    Escape strings when building a new JSON string.

    :meta private:
    """
    if not isinstance(to_escape, str):
        # TODO
        raise TypeError("expected a str")
    # return to_escape
    # TODO ensure_ascii=False = èAnt\\n👍
    # TODO             =True  = \\u00e8Ant\\n\\ud83d\\udc4d'
    # print(f"{to_escape=}")
    # jdumps = json.dumps({"escaped": to_escape}["escaped"])
    # print(f"{jdumps=}")
    return json.dumps({"escaped": to_escape}["escaped"])


def build_dsrc_code_json(dsrc_code: str) -> str:
    """
    Build JSON string of single data source code.

    Input: CUSTOMERS

    Output: {"DSRC_CODE": "CUSTOMERS"}

    :meta private:
    """
    return f'{{"DSRC_CODE": {escape_json_str(dsrc_code)}}}'


def build_data_sources_json(dsrc_codes: list[str]) -> str:
    """
    Build JSON string of data source codes.

    Input: ["REFERENCE", "CUSTOMERS"]

    Output: {"DATA_SOURCES": ["REFERENCE", "CUSTOMERS"]}'

    :meta private:
    """

    dsrcs = ", ".join([f"{escape_json_str(code)}" for code in dsrc_codes])

    return f"{START_DSRC_JSON}{dsrcs}{END_JSON}"


def build_entities_json(entity_ids: Union[List[int], None]) -> str:
    """
    Build JSON string of entity ids.

    Input: [1, 100002]

    Output: {"ENTITIES": [{"ENTITY_ID": 1}, {"ENTITY_ID": 100002}]}

    :meta private:
    """
    if not entity_ids or (isinstance(entity_ids, list) and len(entity_ids) == 0):
        return ""

    entities = ", ".join([f'{{"ENTITY_ID": {id}}}' for id in entity_ids])

    return f"{START_ENTITIES_JSON}{entities}{END_JSON}"


def build_records_json(record_keys: Union[List[tuple[str, str]], None]) -> str:
    """
    Build JSON string of data source and record ids.

    From: [("CUSTOMERS", "1001"), ("WATCHLIST", 1007)]

    To: {"RECORDS":[{"DATA_SOURCE":"CUSTOMERS","RECORD_ID":"1001"},{"DATA_SOURCE":"WATCHLIST","RECORD_ID":"1007"}]}

    :meta private:
    """
    if not record_keys or (isinstance(record_keys, list) and len(record_keys) == 0):
        return ""

    records = ", ".join(
        [
            f'{{"DATA_SOURCE": {escape_json_str(ds)}, "RECORD_ID": {escape_json_str(rec_id)}}}'
            for ds, rec_id in record_keys
        ]
    )

    return f"{START_RECORDS_JSON}{records}{END_JSON}"


# -----------------------------------------------------------------------------
# Helpers for working with parameters
# -----------------------------------------------------------------------------


def as_str(candidate_value: Union[str, Dict[Any, Any]]) -> str:
    """
    Given a string or dict, return a str.

    :meta private:
    """
    if isinstance(candidate_value, dict):
        return json.dumps(candidate_value)

    return candidate_value


# -----------------------------------------------------------------------------
# Helpers for working with C
# -----------------------------------------------------------------------------


def as_c_uintptr_t(candidate_value: int) -> _Pointer[c_uint]:
    """
    This converts many types of values to an integer.

    :meta private:
    """

    # Test if candidate_value can be used with the ctype and is an int. If not a
    # TypeError is raised and caught by the catch_non_sz_exceptions decorator
    _ = c_uint(candidate_value)

    return cast(candidate_value, POINTER(c_uint))


def as_c_char_p(candidate_value: str) -> Any:
    """
    Convert a Python string to bytes.

    :meta private:
    """
    if candidate_value is None:
        return b""

    if isinstance(candidate_value, str):
        return candidate_value.encode()

    return candidate_value


def as_python_str(candidate_value: Any) -> str:
    """
    From a c_char_p, return a python str.

    :meta private:
    """
    result_raw = cast(candidate_value, c_char_p).value
    result = result_raw.decode() if result_raw else ""
    return result


# -----------------------------------------------------------------------------
# Helpers to create Senzing specific exceptions
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# ErrorBuffer class
# -----------------------------------------------------------------------------


class ErrorBuffer(threading.local):
    """
    Buffer to call C

    :meta private:
    """

    # pylint: disable=R0903

    def __init__(self) -> None:
        super().__init__()
        self.string_buffer = create_string_buffer(65535)
        self.string_buffer_size = sizeof(self.string_buffer)


ERROR_BUFFER = ErrorBuffer()
ERROR_BUFFER_TYPE = c_char * 65535


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


def engine_exception(
    get_last_exception: Callable[[_Pointer[c_char], int], str],
    clear_last_exception: Callable[[], None],
    get_last_exception_code: Callable[[], int],
) -> Exception:
    """
    Generate a Senzing error.

    :meta private:
    """
    sz_error_code = get_last_exception_code()
    sz_error_text = get_senzing_error_text(get_last_exception, clear_last_exception)
    senzing_error_class = ENGINE_EXCEPTION_MAP.get(sz_error_code, SzError)
    return senzing_error_class(sz_error_text)


# -----------------------------------------------------------------------------
# Helpers for creating SDK specific exceptions
# -----------------------------------------------------------------------------

# TODO Still needed?
# fmt: off
SDK_EXCEPTION_MAP = {
    1: "failed to load the Senzing library",                                 # Engine module wasn't able to load the G2 library
    2: "instance_name and settings arguments must be specified",        # Engine module constructor didn't receive correct arguments
}
# fmt: on


def sdk_exception(msg_code: int) -> Exception:
    """
    Raise general SzError for SDK issues.

    :meta private:
    """
    return SzError(SDK_EXCEPTION_MAP.get(msg_code, f"No message for index {msg_code}."))
