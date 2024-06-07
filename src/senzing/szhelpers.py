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

from senzing import new_szexception

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

uintptr_type = POINTER(c_uint)
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


# -----------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------


# TODO Not just catching ctypes exceptions, now also catching entity/record json building exceptions
# TODO Change name
def catch_ctypes_exceptions(func_to_decorate: Callable[P, T]) -> Callable[P, T]:
    """# TODO Modify a ctypes.ArgumentError to a TypeError with additional information if exception occurs.
    Also..."""

    @wraps(func_to_decorate)
    # TODO Change name, looks a little odd in traceback
    def inner_function(*args: P.args, **kwargs: P.kwargs) -> T:
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
            # TODO Change to if err.args: instead, more pythonic - need to test
            if len(err.args) >= 1:
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
        # Catch TypeError from the test in as_uintptr_t()
        except TypeError as err:
            raise TypeError(f"{basic_msg} - {err}") from None

    return inner_function


# -----------------------------------------------------------------------------
# Helpers for ...
# -----------------------------------------------------------------------------


# TODO Remove and call directly from each module now other args removed?
def check_result_rc(
    lib_get_last_exception: Callable[[_Pointer[c_char], int], str],
    lib_clear_last_exception: Callable[[], None],
    lib_get_last_exception_code: Callable[[], int],
    # product_id: str,
    # error_id: int,
    result_return_code: int,
) -> None:
    """# TODO"""
    if result_return_code != 0:
        raise new_szexception(
            lib_get_last_exception,
            lib_clear_last_exception,
            lib_get_last_exception_code,
            # product_id,
            # error_id,
        )


# -----------------------------------------------------------------------------
# Helpers for building JSON strings for Senzing engine APIs
# -----------------------------------------------------------------------------


# TODO Improve upon Any?
def check_type_is_list(to_check: Any) -> None:
    """
    Check the input type is a list, if not raise TypeError.

    Args:
        var_to_check (Any): _description_

    Raises:
        TypeError: _description_
    """ """"""
    if not isinstance(to_check, list):
        raise TypeError(f"Expected type list, got {type(to_check).__name__}")


def escape_json_str(to_escape: str, strip_quotes: bool = False) -> str:
    """# TODO"""
    escaped = json.dumps({"escaped": to_escape}["escaped"], ensure_ascii=False)
    # NOTE Remove first and last double quote added by json.dumps()
    if strip_quotes:
        return escaped[1:-1]
    return escaped


def build_dsrc_code_json(dsrc_code: str) -> str:
    """# TODO"""
    # return f'{{"DSRC_CODE": {escape_json_str(dsrc_code)}}}'
    return f'{{"DSRC_CODE": "{dsrc_code}"}}'


def build_data_sources_json(dsrc_codes: list[str]) -> str:
    """
    Build JSON string of data source codes.

    Args:
        dsrc_codes (list[str]): _description_

    Returns:
        str: JSON string as expected by Senzing engine
             {"DATA_SOURCES": ["REFERENCE", "CUSTOMERS"]}'
    """
    check_type_is_list((dsrc_codes))
    dsrcs = ", ".join([f'"{code}"' for code in dsrc_codes])
    return f"{START_DSRC_JSON}{dsrcs}{END_JSON}"


def build_entities_json(entity_ids: list[int]) -> str:
    """
    Build JSON string of entity ids.

    Args:
        entity_ids (list): _description_

    Returns:
        str: JSON string as expected by Senzing engine
             {"ENTITIES": [{"ENTITY_ID": 1}, {"ENTITY_ID": 100002}]}
    """
    check_type_is_list(entity_ids)
    entities = ", ".join([f'{{"ENTITY_ID": {id}}}' for id in entity_ids])
    return f"{START_ENTITIES_JSON}{entities}{END_JSON}"


# TODO What if no ds or id is sent in
# TODO Tests
def build_records_json(record_keys: list[tuple[str, str]]) -> str:
    """# TODO
    Build JSON string of data source and record ids.

    Args:
        record_keys (list): _description_

    Returns:
        str: JSON string as expected by Senzing engine
             {"RECORDS":[{"DATA_SOURCE":"CUSTOMERS","RECORD_ID":"1001"},{"DATA_SOURCE":"WATCHLIST","RECORD_ID":"1007"}]}
    """
    check_type_is_list(record_keys)
    records = ", ".join(
        [
            f'{{"DATA_SOURCE": "{ds}", "RECORD_ID": "{rec_id}"}}'
            # f'{{"DATA_SOURCE": {escape_json_str(ds)}, "RECORD_ID": {escape_json_str(rec_id)}}}'
            for ds, rec_id in record_keys
        ]
    )
    return f"{START_RECORDS_JSON}{records}{END_JSON}"


# TODO Needs testing / tests
# TODO Change name to build avoidances when Jira is complete
def build_exclusions_json(
    input_list: Union[list[int], list[tuple[str, str]], None]
) -> str:
    """
    Build JSON string of either entity ids or data source and record ids.
    Find path exclusions accepts either entity ids or data source and record ids.

    Args:
        input_list (Union[list[int], list[tuple[str, str]], None]): _description_

    Raises:
        TypeError: _description_

    Returns:
        str: _description_
    """ """"""

    # NOTE Testing for None here instead of in szengine to keep szengine "neater" for now
    # NOTE This is needed if required_data_sources is sent to find_path_*, exclusions could
    # NOTE be set to None (default) or []
    # TODO Can this be changed to only if not input_list, more pythonic - need to test
    # TODO recall had to have the len() also to catch something specific?
    if not input_list or len(input_list) == 0:
        return ""

    check_type_is_list(input_list)

    if isinstance(input_list[0], tuple):
        return build_records_json(input_list)  # type: ignore[arg-type]

    if isinstance(input_list[0], int):
        return build_entities_json(input_list)  # type: ignore[arg-type]

    raise TypeError(
        f"Expected a list of ints or tuples, got a list of {type(input_list[0])}"
    )


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
    if isinstance(candidate_value, dict):
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


# TODO Are all these different types needed, we really expect a str?
# TODO as_c_char_p? Returns bytes
def as_c_char_p(candidate_value: Any) -> Any:
    """
    Internal processing function.

    :meta private:
    """

    if isinstance(candidate_value, str):
        return candidate_value.encode()
    if candidate_value is None:
        return b""
    # if isinstance(candidate_value, bytearray):
    #     return candidate_value.decode().encode()
    # if isinstance(candidate_value, bytes):
    #     return str(candidate_value).encode()
    return candidate_value


def as_python_str(candidate_value: Any) -> str:
    """
    From a c_char_p, return a true python str,

    Args:
        candidate_value (Any): A c_char_p value to be transformed.

    Returns:
        str: The python string representation.

    :meta private:
    """
    # TODO catch_exceptions decorator would catch, need to check error type and that it's caught
    result_raw = cast(candidate_value, c_char_p).value
    result = result_raw.decode() if result_raw else ""
    return result


# -----------------------------------------------------------------------------
# Helpers for working with files and directories.
# -----------------------------------------------------------------------------


# TODO ctypes has a function to do this I think I saw?
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
