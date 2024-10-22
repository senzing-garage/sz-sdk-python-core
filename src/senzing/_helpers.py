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
import re
import sys
import threading
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

from senzing_abstract import ENGINE_EXCEPTION_MAP

from senzing import SzError

# if sys.version_info < (3, 10):
if sys.version_info < (3, 11):
    from typing_extensions import ParamSpec, Self
else:
    from typing import ParamSpec, Self

# TODO Add metadata, should use __all__ ?

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
        self.handle.G2GoHelper_free(self.resource)


# -----------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------


# TODO Not just catching ctypes exceptions, now also catching entity/record json building exceptions
# TODO Check functions without try/except are caught by this
def catch_exceptions(func_to_decorate: Callable[P, T]) -> Callable[P, T]:
    """
    # TODO

    :meta private:
    """

    @wraps(func_to_decorate)
    def catch_inner(*args: P.args, **kwargs: P.kwargs) -> T:
        method_name = func_to_decorate.__name__
        module_name = func_to_decorate.__module__
        basic_msg = (
            f"wrong type for an argument when calling {module_name}.{method_name}"
        )

        try:
            return func_to_decorate(*args, **kwargs)
        except ArgumentError as err:
            # Checking can find the information from ctypes.Argument error, works currently but could change in future?
            # If can locate what we are looking for from ctypes.ArgumentError, give a more detailed and useful exception message
            # Current message from ctypes: ctypes.ArgumentError: argument 2: TypeError: wrong type
            bad_arg_match = None
            if err.args:
                bad_arg_match = re.match(r"argument (\d+):", err.args[0])

            if bad_arg_match:
                bad_arg_index = bad_arg_match.group(1)
                try:
                    bad_arg_index = int(bad_arg_index)
                    bad_arg_value = args[bad_arg_index]
                    bad_arg_type = type(bad_arg_value)
                    bad_arg_tuple = list(func_to_decorate.__annotations__.items())[
                        bad_arg_index - 1
                    ]
                except (IndexError, ValueError):
                    raise TypeError(basic_msg) from err

                if len(bad_arg_tuple) != 2:
                    raise TypeError(basic_msg) from err

                raise TypeError(
                    f"wrong type for argument {bad_arg_tuple[0]}, expected {bad_arg_tuple[1]} but received {bad_arg_type.__name__} when calling {module_name}.{method_name}"
                ) from None

            raise TypeError(basic_msg) from err
        # # TODO Do we need to catch anything else? Has a code smell about it
        # NOTE Catch TypeError from the test in as_uintptr_t()
        except TypeError as err:
            raise TypeError(f"{basic_msg} - {err}") from None

    return catch_inner


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
            win_path = find_library(lib if lib else "G2")
            return cdll.LoadLibrary(win_path if win_path else "")

        return cdll.LoadLibrary(lib if lib else "libG2.so")
    except OSError as err:
        # TODO Change to Sz library when the libG2.so is changed in a build
        # TODO Wording & links for V4
        print(
            f"ERROR: Unable to load the Senzing library: {err}\n"
            "ERROR: Did you remember to setup your environment by sourcing the setupEnv file?\n"
            "ERROR: For more information: https://senzing.zendesk.com/hc/en-us/articles/115002408867-Introduction-G2-Quickstart\n"
            "ERROR: If you are running Ubuntu or Debian also review the ssl and crypto information at https://senzing.zendesk.com/hc/en-us/articles/115010259947-System-Requirements\n",
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


def check_type_is_list(to_check: Any) -> None:
    """
    Check the input type is a list, if not raise TypeError.

    :meta private:
    """
    if not isinstance(to_check, list):
        raise TypeError(f"expected type list, got {type(to_check).__name__}")


def check_list_types(to_check: List[Any]) -> None:
    """
    Check the elements of a list for:
        - All the same type
        - If a list of tuples
            - The number of elements in each tuple is the same
            - The number of elements in each tuple is of the expected size

    :meta private:
    """
    if not to_check:
        return

    # Check all elements in the list are of the same type
    types = all(isinstance(elem, type(to_check[0])) for elem in to_check[1:])
    if not types:
        raise TypeError(f"elements in the list are not of the same type - {to_check}")

    # TODO Consider making the number_of_tuples check an input to function
    # If elements are tuples check they are the same size and correct size
    if isinstance(to_check[0], tuple):
        num_elements = set(len(elem) for elem in to_check)
        if len(num_elements) > 1:
            raise TypeError(
                f"number of tuple elements for each tuple are not of the same size - {to_check}"
            )

        number_of_tuples = num_elements.pop()
        if number_of_tuples != 2:
            raise TypeError(
                f"number of elements in a tuple is {number_of_tuples}, expected 2 - {to_check}"
            )


# TODO - Ant - And Jira
def escape_json_str(to_escape: str) -> str:
    """
    Escape strings when building a new JSON string.

    :meta private:
    """
    if not isinstance(to_escape, str):
        raise TypeError(f"expected a str, got{to_escape}")
    # TODO ensure_ascii=False = èAnt\\n👍
    # TODO             =True  = \\u00e8Ant\\n\\ud83d\\udc4d'
    print(f"{to_escape = }")
    jdumps = json.dumps({"escaped": to_escape}["escaped"])
    print(f"{jdumps = }")
    return json.dumps({"escaped": to_escape}["escaped"])


def build_dsrc_code_json(dsrc_code: str) -> str:
    """
    Build JSON string of single data source code.

    {"DSRC_CODE": "CUSTOMERS"}

    :meta private:
    """
    return f'{{"DSRC_CODE": {escape_json_str(dsrc_code)}}}'


def build_data_sources_json(dsrc_codes: list[str]) -> str:
    """
    Build JSON string of data source codes.

    {"DATA_SOURCES": ["REFERENCE", "CUSTOMERS"]}'

    :meta private:
    """
    check_type_is_list((dsrc_codes))
    check_list_types(dsrc_codes)
    dsrcs = ", ".join([f"{escape_json_str(code)}" for code in dsrc_codes])
    return f"{START_DSRC_JSON}{dsrcs}{END_JSON}"


# TODO Additional checks on these functions
def build_entities_json(entity_ids: Union[List[int], None]) -> str:
    """
    Build JSON string of entity ids.

    {"ENTITIES": [{"ENTITY_ID": 1}, {"ENTITY_ID": 100002}]}

    :meta private:
    """
    # NOTE This is needed if required_data_sources is sent to find_path_*, avoid_* could
    # NOTE be set to None (default) or []
    if not entity_ids or len(entity_ids) == 0:
        return ""

    check_type_is_list(entity_ids)
    check_list_types(entity_ids)
    entities = ", ".join([f'{{"ENTITY_ID": {id}}}' for id in entity_ids])
    return f"{START_ENTITIES_JSON}{entities}{END_JSON}"


def build_records_json(record_keys: Union[List[tuple[str, str]], None]) -> str:
    """
    Build JSON string of data source and record ids.

    {"RECORDS":[{"DATA_SOURCE":"CUSTOMERS","RECORD_ID":"1001"},{"DATA_SOURCE":"WATCHLIST","RECORD_ID":"1007"}]}

    :meta private:
    """
    # NOTE This is needed if required_data_sources is sent to find_path_*, avoid_* could
    # NOTE be set to None (default) or []
    if not record_keys or len(record_keys) == 0:
        return ""

    check_type_is_list(record_keys)
    check_list_types(record_keys)
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
    # TypeError is raised and caught by the catch_exceptions decorator on
    # calling methods
    # TODO Better to raise here?
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
    # TODO catch_exceptions decorator would catch, need to check error type and that it's caught
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
    Generate a new Senzing Exception based on the SDK product_id & error_id.

    :meta private:
    """
    sz_error_code = get_last_exception_code()
    sz_error_text = get_senzing_error_text(get_last_exception, clear_last_exception)
    senzing_error_class = ENGINE_EXCEPTION_MAP.get(sz_error_code, SzError)
    return senzing_error_class(sz_error_text)


# -----------------------------------------------------------------------------
# Helpers for creating SDK specific exceptions
# -----------------------------------------------------------------------------

# fmt: off
SDK_EXCEPTION_MAP = {
    1: "failed to load the G2 library",                                 # Engine module wasn't able to load the G2 library
    2: "instance_name and settings arguments must be specified",        # Engine module constructor didn't receive correct arguments
}
# fmt: on


def sdk_exception(msg_code: int) -> Exception:
    """
    Raise general SzError for SDK issues.

    :meta private:
    """
    return SzError(SDK_EXCEPTION_MAP.get(msg_code, f"No message for index {msg_code}."))
