"""
SDK Helper functions
"""

# NOTE - This is to prevent TypeError: '_ctypes.PyCPointerType' object is not subscriptable  on _Pointer[c_char]) for
# NOTE - FreeCResources ctypes._Pointer is generic for type checkers, but at runtime it's not generic, so annotations
# NOTE - import is necessary - or string annotation ("_Pointer[c_char]") .
from __future__ import annotations

import platform
import threading
from collections.abc import Callable
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
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from typing import cast as typing_cast

from senzing import ENGINE_EXCEPTION_MAP, SzError, SzSdkError

try:
    import orjson  # type: ignore[import-not-found]

    def _json_dumps(object_: Any) -> str:
        return orjson.dumps(object_).decode("utf-8")  # type: ignore

except ImportError:
    import json

    # NOTE - separators= is used to be consistent with Sz engine and orjson output
    def _json_dumps(object_: Any) -> str:
        return json.dumps(object_, ensure_ascii=False, separators=(",", ":"))


# NOTE - Using earlier Python version typing to support v3.9 still and not rely on typing_extensions.
# NOTE - F can be changed to use ParamSpec when no longer need to support v3.9.
# NOTE - SelfFreeCResources can be changed to use Self at v3.11.
F = TypeVar("F", bound=Callable[..., Any])
SelfFreeCResources = TypeVar("SelfFreeCResources", bound="FreeCResources")

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

    def __enter__(self: SelfFreeCResources) -> SelfFreeCResources:
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


# def catch_sdk_exceptions(func_to_decorate: Callable[P, T]) -> Callable[P, T]:
def catch_sdk_exceptions(func_to_decorate: F) -> F:
    """
    The Python SDK methods convert Python types to ctypes and utilize helper functions. If incorrect types/values are
    used standard library exceptions are raised not SzError exceptions as the Senzing library hasn't been called
    yet. Raise the original Python exception type and append information to identify the SDK method called, accepted
    arguments & types and the arguments and types the SDK method received. Also convert ctypes.ArgumentError exceptions
    to TypeError, a user shouldn't need to import ctypes to catch ArgumentError

    :meta private:
    """

    @wraps(func_to_decorate)
    def wrapped_func(*args: Any, **kwargs: Any) -> F:
        try:
            return typing_cast(F, func_to_decorate(*args, **kwargs))
        except (ArgumentError, TypeError, ValueError) as err:
            # Get wrapped function annotation, remove unwanted keys
            annotations_dict = func_to_decorate.__annotations__
            with suppress(KeyError):
                del annotations_dict["return"]
                del annotations_dict["kwargs"]

            # Get the wrapped function signature names and types and build a string to append to the error message
            func_signature = ", ".join(
                [
                    f"{name}: {type if isinstance(type, str) else type.__name__}"
                    for name, type in annotations_dict.items()
                ]
            )

            method_and_signature = f"{func_to_decorate.__module__}.{func_to_decorate.__name__}({func_signature})"
            append_err_msg = f" - expected: {method_and_signature}"

            arg_0 = err.args[0]
            if " missing " in err.args[0] and " required positional argument" in err.args[0]:
                arg_0 = " ".join(err.args[0].split()[1:])
            new_arg_0 = f"calling {method_and_signature}" if not err.args else f"{arg_0}{append_err_msg}"
            err.args = (new_arg_0,) + err.args[1:]

            raise SzSdkError(err) from err

    return typing_cast(F, wrapped_func)


# -----------------------------------------------------------------------------
# Helpers for loading Senzing C library
# -----------------------------------------------------------------------------
def load_sz_library(lib: str = "", os: str = "") -> CDLL:
    """
    Check the OS name and load the appropriate Senzing library.

    :meta private:
    """

    system_name = os if os else platform.uname().system

    try:
        if system_name == "Linux":
            return cdll.LoadLibrary(lib if lib else "libSz.so")

        if system_name == "Darwin":
            return cdll.LoadLibrary(lib if lib else "libSz.dylib")

        if system_name == "Windows":
            win_path = find_library(lib if lib else "Sz")
            return cdll.LoadLibrary(win_path if win_path else "")

        raise SzSdkError(f"{system_name} is an unsupported operating system")
    except OSError as err:
        # TODO - Wording & links for V4
        print(
            f"ERROR: Unable to load the Senzing library: {err}\n"
            "       Did you remember to setup your environment by sourcing the setupEnv file?\n"
            "       For more information: https://senzing.zendesk.com/hc/en-us/articles/115002408867-Introduction-G2-Quickstart\n"
            "       If you are running Ubuntu or Debian also review the ssl and crypto information at https://senzing.zendesk.com/hc/en-us/articles/115010259947-System-Requirements\n",
        )
        raise SzSdkError("failed to load the Senzing library") from err


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


def escape_json_str(to_escape: str) -> str:
    """
    Escape strings when building a new JSON string. Glyphs, emojis, etc are not converted to ASCII code points. UTF-8 code
    points are converted to their glyphs, emojis, etc.

    :meta private:
    """
    if not isinstance(to_escape, str):
        raise TypeError(f"value {to_escape} has type {type(to_escape).__name__}, should be a str")

    return _json_dumps(to_escape)


def build_dsrc_code_json(dsrc_code: str) -> str:
    """
    Build JSON string of single data source code.

    Input: CUSTOMERS

    Output: {"DSRC_CODE": "CUSTOMERS"}

    :meta private:
    """
    if not isinstance(dsrc_code, str):
        raise TypeError(f"value {dsrc_code} has type {type(dsrc_code).__name__}, should be a str")

    return f'{{"DSRC_CODE": {escape_json_str(dsrc_code)}}}'


def build_data_sources_json(dsrc_codes: list[str]) -> str:
    """
    Build JSON string of data source codes.

    Input: ["REFERENCE", "CUSTOMERS"]

    Output: {"DATA_SOURCES": ["REFERENCE", "CUSTOMERS"]}'

    :meta private:
    """
    if not isinstance(dsrc_codes, list):
        raise TypeError(f"value {dsrc_codes} has type {type(dsrc_codes).__name__}, should be a list")

    if not all(isinstance(d, str) for d in dsrc_codes):
        element_types_str = ", ".join({type(t).__name__ for t in dsrc_codes if not isinstance(t, str)})
        raise TypeError(f"elements in {dsrc_codes} should be str(s), there are {element_types_str}")

    dsrcs_str = ", ".join([f"{escape_json_str(code)}" for code in dsrc_codes])

    return f"{START_DSRC_JSON}{dsrcs_str}{END_JSON}"


def build_entities_json(entity_ids: Union[List[int], None]) -> str:
    """
    Build JSON string of entity ids.

    Input: [1, 100002]

    Output: {"ENTITIES": [{"ENTITY_ID": 1}, {"ENTITY_ID": 100002}]}

    :meta private:
    """
    if not entity_ids or (isinstance(entity_ids, list) and len(entity_ids) == 0):
        return ""

    if not isinstance(entity_ids, list):
        raise TypeError(f"value {entity_ids} has type {type(entity_ids).__name__}, should be a list of int(s)")

    if not all(isinstance(e, int) for e in entity_ids):
        element_types_str = ", ".join({type(t).__name__ for t in entity_ids if not isinstance(t, int)})
        raise TypeError(f"elements in {entity_ids} should be int(s), there are {element_types_str}")

    eids_str = ", ".join([f'{{"ENTITY_ID": {id}}}' for id in entity_ids])

    return f"{START_ENTITIES_JSON}{eids_str}{END_JSON}"


def build_records_json(record_keys: Union[List[tuple[str, str]], None]) -> str:
    """
    Build JSON string of data source and record ids.

    Input: [("CUSTOMERS", "1001"), ("WATCHLIST", "1007")]

    Output: {"RECORDS":[{"DATA_SOURCE":"CUSTOMERS","RECORD_ID":"1001"},{"DATA_SOURCE":"WATCHLIST","RECORD_ID":"1007"}]}

    :meta private:
    """
    if not record_keys or (isinstance(record_keys, list) and len(record_keys) == 0):
        return ""

    record_keys_with_elements = [rk for rk in record_keys if rk]
    wrong_types = set()

    if not all(isinstance(e, tuple) for e in record_keys_with_elements):
        element_types_str = ", ".join({type(t).__name__ for t in record_keys_with_elements if not isinstance(t, tuple)})
        raise TypeError(f"elements in {record_keys} should be tuple(s), there are {element_types_str}")

    if not all({len(e) == 2 for e in record_keys_with_elements}):
        element_len_str = ", ".join({str(len(t)) for t in record_keys_with_elements})
        raise TypeError(f"tuple(s) length in {record_keys} should be 2, there are lengths(s) of {element_len_str}")

    if rk_wrong_types := [
        rk for rk in record_keys_with_elements if not isinstance(rk[0], str) or not isinstance(rk[1], str)
    ]:
        wrong_types = {(type(w[0]).__name__, type(w[1]).__name__) for w in rk_wrong_types}

    if wrong_types:
        wrong_types_str = ", ".join({f"({wt[0]}, {wt[1]})" for wt in wrong_types})
        raise TypeError(f"tuple(s) types in {record_keys} should be (str, str), there are {wrong_types_str}")

    records = ", ".join(
        [
            f'{{"DATA_SOURCE": {escape_json_str(ds)}, "RECORD_ID": {escape_json_str(rec_id)}}}'
            for ds, rec_id in record_keys_with_elements
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
        return _json_dumps(candidate_value)

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
    # TypeError is raised and caught by the catch_sdk_exceptions decorator
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
    return result_raw.decode() if result_raw else ""


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
