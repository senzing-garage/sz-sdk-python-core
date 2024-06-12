import json

import pytest
from pytest_schema import schema

from senzing import SzError
from senzing._helpers import (
    as_c_char_p,
    as_str,
    build_data_sources_json,
    check_type_is_list,
    load_sz_library,
)

# -----------------------------------------------------------------------------
# szhelpers testcases
# -----------------------------------------------------------------------------


def test_as_c_char_p() -> None:
    """# TODO"""
    a_string = "This is a test string"
    actual = as_c_char_p(a_string)
    assert isinstance(actual, bytes)


def test_as_c_char_p_none() -> None:
    """# TODO"""
    actual = as_c_char_p(None)
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


def test_check_type_is_list() -> None:
    """# TODO"""
    list_ = [1, 2, 3]
    check_type_is_list(list_)


def test_check_type_is_list_bad_type() -> None:
    """# TODO"""
    list_ = "not_a_list"
    with pytest.raises(TypeError):
        check_type_is_list(list_)


# TODO Will need additional logic for Windows
def test_load_sz_library_missing_lib() -> None:
    """# TODO"""
    lib_file = "non_exist_file"
    with pytest.raises(SzError):
        actual = load_sz_library(lib=lib_file)
        assert isinstance(actual, SzError)


# -----------------------------------------------------------------------------
# _helpers schemas
# -----------------------------------------------------------------------------

build_data_sources_json_schema = {"DATA_SOURCES": [str]}

build_avoidances_json_by_entity_id_schema = {"ENTITIES": [{"ENTITY_ID": int}]}

build_avoidances_json_by_record_keys_schema = {
    "RECORDS": [{"DATA_SOURCE": str, "RECORD_ID": str}]
}
# "RECORDS":[{"DATA_SOURCE":"CUSTOMERS","RECORD_ID":"1001"},{"DATA_SOURCE":"WATCHLIST","RECORD_ID":"1007"}]}
