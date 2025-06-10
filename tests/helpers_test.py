import json

import pytest
from pytest_schema import schema
from senzing import SzError

from senzing_core._helpers import (
    as_c_char_p,
    as_str,
    build_data_sources_json,
    build_dsrc_code_json,
    build_entities_json,
    build_records_json,
    escape_json_str,
    load_sz_library,
)

# -----------------------------------------------------------------------------
# szhelpers testcases
# -----------------------------------------------------------------------------


def test_as_python_bytes() -> None:
    """Test as_c_char_p()."""
    a_string = "This is a test string"
    actual = as_c_char_p(a_string)
    assert isinstance(actual, bytes)


def test_as_python_bytes_none() -> None:
    """Test as_c_char_p() with None."""
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
    actual = json.dumps(a_dict, separators=(",", ":"))
    result1 = as_str(a_dict)
    assert isinstance(result1, str)
    assert result1 == actual
    result2 = as_str(actual)
    assert isinstance(result2, str)
    assert result2 == actual


def test_build_data_source_json() -> None:
    """Test build_dsrc_code_json()."""
    data_source = "CUSTOMERS"
    actual = build_dsrc_code_json(data_source)
    assert isinstance(actual, str)
    actual_as_dict = json.loads(actual)
    assert schema(build_data_source_json_schema) == actual_as_dict


def test_build_data_source_json_bad_type() -> None:
    """Test build_dsrc_code_json()."""
    with pytest.raises(TypeError):
        build_dsrc_code_json(1234)  # type: ignore[arg-type]


def test_build_data_sources_json() -> None:
    """Test build_data_sources_json()."""
    data_sources = ["TESTONE", "TESTTWO"]
    actual = build_data_sources_json(data_sources)
    assert isinstance(actual, str)
    actual_as_dict = json.loads(actual)
    assert schema(build_data_sources_json_schema) == actual_as_dict


def test_build_data_sources_json_bad_type() -> None:
    """Test build_data_sources_json()."""
    with pytest.raises(TypeError):
        build_data_sources_json(1234)  # type: ignore[arg-type]


def test_build_data_sources_json_bad_element_type() -> None:
    """Test build_data_sources_json()."""
    with pytest.raises(TypeError):
        build_data_sources_json(["TEST", 1, 2])  # type: ignore[list-item]


def test_build_entities_json() -> None:
    """Test build_entities_json()."""
    actual = build_entities_json([1, 100002])
    assert isinstance(actual, str)
    actual_as_dict = json.loads(actual)
    assert schema(build_entities_json_schema) == actual_as_dict


def test_build_entities_json_empty_list() -> None:
    """Test build_entities_json()."""
    actual = build_entities_json([])
    assert isinstance(actual, str)
    assert len(actual) == 0


def test_build_entities_json_bad_type() -> None:
    """Test build_entities_json()."""
    with pytest.raises(TypeError):
        build_entities_json(1234)  # type: ignore[arg-type]


def test_build_entities_json_bad_element_type() -> None:
    """Test build_entities_json()."""
    with pytest.raises(TypeError):
        build_entities_json(["TEST", 1, 2])  # type: ignore[list-item]


def test_build_records_json() -> None:
    """Test build_records_json()."""
    actual = build_records_json([("CUSTOMERS", "1001"), ("WATCHLIST", "1007")])
    assert isinstance(actual, str)
    actual_as_dict = json.loads(actual)
    assert schema(build_records_json_schema) == actual_as_dict


def test_build_records_json_empty_list() -> None:
    """Test build_records_json()."""
    actual = build_records_json([])
    assert isinstance(actual, str)
    assert len(actual) == 0


def test_build_records_json_bad_type() -> None:
    """Test build_records_json()."""
    with pytest.raises(TypeError):
        build_records_json(1234)  # type: ignore[arg-type]


def test_build_records_json_bad_element_type() -> None:
    """Test build_records_json()."""
    with pytest.raises(TypeError):
        build_records_json(["CUSTOMERS", "WATCHLIST"])  # type: ignore[list-item]


def test_build_records_json_tuple_wrong_length() -> None:
    """Test build_records_json()."""
    with pytest.raises(TypeError):
        build_records_json([("CUSTOMERS", "1001", 1234)])  # type: ignore[list-item]


def test_build_records_json_tuple_element_wrong_type() -> None:
    """Test build_records_json()."""
    with pytest.raises(TypeError):
        build_records_json([("CUSTOMERS", 1001), ("WATCHLIST", 1007)])  # type: ignore[list-item]


def test_escape_json_str() -> None:
    """Test build_records_json()."""
    actual = escape_json_str('Testing"')
    assert isinstance(actual, str)


# Black formatting is turned off so as not to rewrite strings to Python equivalent and remove quotes and /
# fmt: off
def test_escape_json_str_double_quote() -> None:
    """Test escape_json_str()."""
    a_string = 'Testing"'
    actual = escape_json_str(a_string)
    assert actual == '"Testing\\""'


def test_escape_json_str_omega() -> None:
    """Test escape_json_str()."""
    a_string = "TestingΩ"
    actual = escape_json_str(a_string)
    assert actual == '"TestingΩ"'


def test_escape_json_str_escaped_omega() -> None:
    """Test escape_json_str()."""
    a_string = "Testing\u03a9"
    actual = escape_json_str(a_string)
    assert actual == '"TestingΩ"'


def test_escape_json_str_emoji() -> None:
    """Test escape_json_str()."""
    a_string = "Testing🤗"
    actual = escape_json_str(a_string)
    assert actual == '"Testing🤗"'


def test_escape_json_str_escaped_emoji() -> None:
    """Test escape_json_str()."""
    a_string = "Testing\U0001f917"
    actual = escape_json_str(a_string)
    assert actual == '"Testing🤗"'
# fmt: on


def test_escape_json_str_bad_type() -> None:
    """Test escape_json_str()."""
    with pytest.raises(TypeError):
        escape_json_str(1234)  # type: ignore[arg-type]


def test_load_sz_library_missing_lib() -> None:
    """Test load_sz_library()."""
    lib_file = "non_exist_file"
    with pytest.raises(SzError):
        actual = load_sz_library(lib=lib_file)
        assert isinstance(actual, SzError)


def test_load_sz_library_incorrect_os() -> None:
    """Test load_sz_library()."""
    os = "Android"
    with pytest.raises(SzError):
        actual = load_sz_library(os=os)
        assert isinstance(actual, SzError)


# -----------------------------------------------------------------------------
# _helpers schemas
# -----------------------------------------------------------------------------

build_data_source_json_schema = {"DSRC_CODE": str}

build_data_sources_json_schema = {"DATA_SOURCES": [str]}

build_entities_json_schema = {"ENTITIES": [{"ENTITY_ID": int}]}

build_records_json_schema = {"RECORDS": [{"DATA_SOURCE": str, "RECORD_ID": str}]}

build_avoidances_json_by_entity_id_schema = {"ENTITIES": [{"ENTITY_ID": int}]}

build_avoidances_json_by_record_keys_schema = {"RECORDS": [{"DATA_SOURCE": str, "RECORD_ID": str}]}
