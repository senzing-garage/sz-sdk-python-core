"""
TODO: szhelpers.py
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
from ctypes import (
    CDLL,
    POINTER,
    ArgumentError,
    _Pointer,
    c_char,
    c_char_p,
    c_uint,
    cast,
)
from functools import wraps
from types import TracebackType
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

# NOTE import orjson if available, on a basic loads it is at least 12% faster on a decently sized getentity and higher for other operations
# with suppress(ModuleNotFoundError):
#     import orjson

uintptr_type = POINTER(c_uint)
T = TypeVar("T")
P = ParamSpec("P")

# ORJSON_AVAILABLE = "orjson" in dir()

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------


class FreeCResources:
    """Free C resources"""

    def __init__(self, handle: CDLL, resource: _Pointer[c_char]) -> None:
        self.handle = handle
        self.resource = resource

    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.handle.G2GoHelper_free(self.resource)


# class SzJsonString(str):
#     """Normally return a JSON string representation of a response from a method call.
#     Return a dictionary of the string response if .as_dict() is specified."""

#     def __init__(self, json_string: str):
#         self.json_string = json_string
#         print(f"{ORJSON_AVAILABLE = }")

#     # NOTE json.loads() is always Any, need union if return string when not JSON
#     # NOTE https://stackoverflow.com/questions/76759158/type-hinting-a-json-object-in-python
#     # NOTE "Even the good people at typeshed use Any as the return type for json.load/json.loads to this day. And they basically maintain the official type stubs for the standard library."
#     # NOTE https://github.com/python/typeshed/blob/f2ee9e9368a18b19bbf2ac05b6eb6bfea96d9a0c/stdlib/json/__init__.pyi#L39-L60
#     # NOTE Using Any will impact automatic documentation generation if szhelpers gets documented?

#     def as_dict(self) -> Any:
#         # TODO: Add check to ensure json_string looks like JSON, is it needed? It's the engines methods using the class not customers.
#         # if re.match("^{.*}$", self.json_string):
#         #     return json.loads(self.json_string)
#         # return self.json_string
#         # TODO: What if the loads fails?
#         if ORJSON_AVAILABLE:
#             return orjson.loads(self.json_string).decode()
#         return json.loads(self.json_string)


# -----------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------


def catch_ctypes_exceptions(function_to_decorate: Callable[P, T]) -> Callable[P, T]:
    # TODO doc string
    """Modify a ctypes.ArgumentError to a TypeError with additional information if exception occurs.
    Also..."""

    @wraps(function_to_decorate)
    def inner_function(*args: P.args, **kwargs: P.kwargs) -> T:
        method_name = function_to_decorate.__name__
        module_name = function_to_decorate.__module__
        basic_msg = (
            f"wrong type for an argument when calling {module_name}.{method_name}"
        )

        try:
            return function_to_decorate(*args, **kwargs)
        except ArgumentError as err:
            # Checking can find the information from ctypes.Argument error, works currently but could change in future?
            # If can locate what we are looking for from ctypes.ArgumentError, give a more detailed and useful exception message
            # Current message from ctypes: ctypes.ArgumentError: argument 2: TypeError: wrong type
            bad_arg_match = None
            if len(err.args) >= 1:
                bad_arg_match = re.match(r"argument (\d+):", err.args[0])

            if bad_arg_match:
                bad_arg_index = bad_arg_match.group(1)
                try:
                    bad_arg_index = int(bad_arg_index)
                    bad_arg_value = args[bad_arg_index]
                    bad_arg_type = type(bad_arg_value)
                    bad_arg_tuple = list(function_to_decorate.__annotations__.items())[
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
        # # NOTE Do we need to catch anything else? Has a code smell about it
        # TODO: Is this generic catch needed?
        # except Exception as err:
        #     # print(f"In szhelpers last exception: {err}")
        #     raise err
        # Catch TypeError from the test in as_uintptr_t()
        except TypeError as err:
            raise TypeError(f"{basic_msg} - {err}") from None

    return inner_function


# -----------------------------------------------------------------------------
# Helpers for working with parameters
# -----------------------------------------------------------------------------


def as_str(candidate_value: Union[str, Dict[Any, Any]]) -> str:
    """
    Given a string or dict, return a str.

    Args:
        candidate_value Union[str, Dict[Any, Any]]: _description_

    Returns:
        str: The string representation of the candidate_value
    """
    # NOTE Testing
    # TODO Are we allowing dicts anywhere in core?
    if isinstance(candidate_value, dict):
        # if ORJSON_AVAILABLE:
        #     return orjson.dumps(candidate_value).decode()
        return json.dumps(candidate_value)
    return candidate_value


# -----------------------------------------------------------------------------
# Helpers for working with C
# -----------------------------------------------------------------------------


# TODO: Figure out better return type hint (e.g. POINTER[c_uint], _Pointer[c_uint])
def as_uintptr_t(candidate_value: int) -> Any:
    """
    Internal processing function.
    This converts many types of values to an integer.

    :meta private:
    """

    # TODO Is this an acceptable approach?
    # Test if candidate_value can be used with the ctype and is an int. If not a
    # TypeError is raised and caught by the catch_ctypes_exceptions decorator on
    # calling methods
    _ = c_uint(candidate_value)

    return cast(candidate_value, POINTER(c_uint))


# NOTE Believe not needed with catch_ctypes_exceptions decorator and this code would
# NOTE would return ValueErrors if a str with any non digit characters was passed in
def as_c_int(candidate_value: Any) -> int:
    """
    Internal processing function.
    This converts many types of values to an integer.

    :meta private:
    """

    if candidate_value is None:  # handle null string
        # TODO: Doesn't need int
        return int(0)
    if isinstance(candidate_value, str):  # if string is unicode, transcode to utf-8 str
        return int(candidate_value.encode("utf-8"))
    if isinstance(
        candidate_value, bytearray
    ):  # if input is bytearray, assume utf-8 and convert to str
        return int(candidate_value)
    if isinstance(candidate_value, bytes):
        return int(candidate_value)
    # TODO: If already an int why use int()?
    # input is already an int
    return int(candidate_value)


def as_c_char_p(candidate_value: Any) -> Any:
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
    ):  # if input is bytearray, assume utf-8 and convert to str
        return candidate_value.decode().encode("utf-8")
    if isinstance(candidate_value, bytes):
        return str(candidate_value).encode("utf-8")
    # input is already a str
    return candidate_value
    # raise TypeError(
    #     f"{candidate_value} has unsupported type of {type(candidate_value)}"
    # )


# NOTE Don't believe need anymore,,,
# def as_python_int(candidate_value: Any) -> int:
#     """
#     From a c_void_p, return a true python int.

#     Args:
#         candidate_value (Any): A c_void_p to be transformed.

#     Returns:
#         int: The python int representation

#     :meta private:
#     """

#     result = cast(candidate_value, c_void_p).value
#     # TODO: For methods using this could we get a non zero return code and return None?
#     # TODO: Would never reach the return as_python_int(result.response) is non zero return code
#     # TODO: Consequences of returning a 0 which wouldn't be a valid handle?
#     if result is None:
#         result = 0
#     return result


def as_python_str(candidate_value: Any) -> str:
    """
    From a c_char_p, return a true python str,

    Args:
        candidate_value (Any): A c_char_p value to be transformed.

    Returns:
        str: The python string representation.

    :meta private:
    """
    # TODO: Do these functions need try/except?
    result_raw = cast(candidate_value, c_char_p).value
    result = result_raw.decode() if result_raw else ""
    return result


# -----------------------------------------------------------------------------
# Helpers for working with files and directories.
# -----------------------------------------------------------------------------


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
