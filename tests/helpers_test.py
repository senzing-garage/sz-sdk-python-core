import json

import pytest
from pytest_schema import schema
from senzing import SzError

from senzing_core._helpers import (
    as_c_char_p,
    as_str,
    build_data_sources_json,
    build_entities_json,
    build_records_json,
    escape_json_str,
    load_sz_library,
)

# -----------------------------------------------------------------------------
# szhelpers testcases
# -----------------------------------------------------------------------------


def test_as_python_bytes() -> None:
    """# TODO"""
    a_string = "This is a test string"
    actual = as_c_char_p(a_string)
    assert isinstance(actual, bytes)


def test_as_python_bytes_none() -> None:
    """# TODO"""
    actual = as_c_char_p(None)  # type: ignore[arg-type]
    assert isinstance(actual, bytes)
    assert len(actual) == 0


def test_as_str() -> None:
    """Test as_str."""
    a_dict = {
        "test1": "Fred",
        "test2": 5,
        "test3": {"test3.1": "Wilma"},
    }
    # actual = json.dumps(a_dict, separators=(",", ":"))
    actual = json.dumps(a_dict)
    result1 = as_str(a_dict)
    assert isinstance(result1, str)
    assert result1 == actual
    result2 = as_str(actual)
    assert isinstance(result2, str)
    assert result2 == actual


def test_build_data_sources_json() -> None:
    """# TODO"""
    data_sources = ["TESTONE", "TESTTWO"]
    actual = build_data_sources_json(data_sources)
    assert isinstance(actual, str)
    actual_as_dict = json.loads(actual)
    assert schema(build_data_sources_json_schema) == actual_as_dict


def test_build_entities_json_empty_list() -> None:
    """# TODO"""
    actual = build_entities_json([])
    assert isinstance(actual, str)
    assert len(actual) == 0


def test_build_records_json_empty_list() -> None:
    """# TODO"""
    actual = build_records_json([])
    assert isinstance(actual, str)
    assert len(actual) == 0


def test_escape_json_str() -> None:
    """# TODO"""
    with pytest.raises(TypeError):
        escape_json_str(1234)  # type: ignore[arg-type]


# TODO Will need additional logic for Windows
def test_load_sz_library_missing_lib() -> None:
    """# TODO"""
    lib_file = "non_exist_file"
    with pytest.raises(SzError):
        actual = load_sz_library(lib=lib_file)
        assert isinstance(actual, SzError)


def test_load_sz_library_incorrect_os() -> None:
    """# TODO"""
    os = "Android"
    with pytest.raises(SzError):
        actual = load_sz_library(os=os)
        assert isinstance(actual, SzError)


# -----------------------------------------------------------------------------
# _helpers schemas
# -----------------------------------------------------------------------------

build_data_sources_json_schema = {"DATA_SOURCES": [str]}

build_avoidances_json_by_entity_id_schema = {"ENTITIES": [{"ENTITY_ID": int}]}

build_avoidances_json_by_record_keys_schema = {"RECORDS": [{"DATA_SOURCE": str, "RECORD_ID": str}]}
# "RECORDS":[{"DATA_SOURCE":"CUSTOMERS","RECORD_ID":"1001"},{"DATA_SOURCE":"WATCHLIST","RECORD_ID":"1007"}]}
