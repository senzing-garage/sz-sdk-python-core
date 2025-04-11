# pylint: disable=C0302

import json
from typing import Any, Dict, List, Tuple

import pytest
from pytest_schema import Optional, Or, schema
from senzing import (
    SZ_NO_FLAGS,
    SZ_WITHOUT_INFO,
    SzBadInputError,
    SzConfig,
    SzConfigManager,
    SzEngine,
    SzEngineFlags,
    SzError,
    SzNotFoundError,
    SzUnknownDataSourceError,
)
from senzing_truthset import (
    TRUTHSET_CUSTOMER_RECORDS,
    TRUTHSET_DATASOURCES,
    TRUTHSET_REFERENCE_RECORDS,
    TRUTHSET_WATCHLIST_RECORDS,
)

from senzing_core import SzConfigCore, SzConfigManagerCore, SzEngineCore

DATA_SOURCES = {
    "CUSTOMERS": TRUTHSET_CUSTOMER_RECORDS,
    "REFERENCE": TRUTHSET_REFERENCE_RECORDS,
    "WATCHLIST": TRUTHSET_WATCHLIST_RECORDS,
}

RECORD_DICT = {
    "RECORD_TYPE": "PERSON",
    "PRIMARY_NAME_LAST": "Smith",
    "PRIMARY_NAME_FIRST": "Robert",
    "DATE_OF_BIRTH": "12/11/1978",
    "ADDR_TYPE": "MAILING",
    "ADDR_LINE1": "123 Main Street, Las Vegas NV 89132",
    "PHONE_TYPE": "HOME",
    "PHONE_NUMBER": "702-919-1300",
    "EMAIL_ADDRESS": "bsmith@work.com",
    "DATE": "1/2/18",
    "STATUS": "Active",
    "AMOUNT": "100",
}

RECORD_STR = (
    '{"RECORD_TYPE": "PERSON", "PRIMARY_NAME_LAST": "Smith", "PRIMARY_NAME_FIRST":'
    ' "Robert", "DATE_OF_BIRTH": "12/11/1978", "ADDR_TYPE": "MAILING", "ADDR_LINE1":'
    ' "123 Main Street, Las Vegas NV 89132","PHONE_TYPE": "HOME", "PHONE_NUMBER":'
    ' "702-919-1300", "EMAIL_ADDRESS": "bsmith@work.com", "DATE": "1/2/18", "STATUS":'
    ' "Active", "AMOUNT": "100"}'
)

RECORD_STR_BAD = (
    '{"RECORD_TYPE": "PERSON" "PRIMARY_NAME_LAST": "Smith", "PRIMARY_NAME_FIRST":'
    ' "Robert", "DATE_OF_BIRTH": "12/11/1978", "ADDR_TYPE": "MAILING", "ADDR_LINE1":'
    ' "123 Main Street, Las Vegas NV 89132","PHONE_TYPE": "HOME", "PHONE_NUMBER":'
    ' "702-919-1300", "EMAIL_ADDRESS": "bsmith@work.com", "DATE": "1/2/18", "STATUS":'
    ' "Active", "AMOUNT": "100"}'
)

# -----------------------------------------------------------------------------
# Pre testcases
# -----------------------------------------------------------------------------


def test_add_truthset_datasources(
    sz_engine: SzEngineCore,
    sz_configmanager: SzConfigManager,
    sz_config: SzConfig,
) -> None:
    """Add needed datasources for tests."""
    config_handle = sz_config.create_config()
    for data_source_code in TRUTHSET_DATASOURCES:
        sz_config.add_data_source(config_handle, data_source_code)
    config_definition = sz_config.export_config(config_handle)
    config_id = sz_configmanager.add_config(config_definition, "Test")
    sz_configmanager.set_default_config_id(config_id)
    sz_engine._reinitialize(config_id)  # pylint: disable=W0212


# -----------------------------------------------------------------------------
# Testcases
# -----------------------------------------------------------------------------


def test_add_record(sz_engine: SzEngine) -> None:
    """Test SzEngine().add_record()."""
    data_source_code = "TEST"
    record_id = "1"
    record_definition: Dict[Any, Any] = {}
    flags = SZ_WITHOUT_INFO
    actual = sz_engine.add_record(data_source_code, record_id, json.dumps(record_definition), flags)
    assert actual == ""


def test_add_record_bad_data_source_code_type(sz_engine: SzEngine) -> None:
    """Test SzEngine().add_record()."""
    bad_data_source_code = 1
    record_id = "1"
    record_definition: Dict[Any, Any] = {}
    flags = SZ_WITHOUT_INFO
    with pytest.raises(TypeError):
        sz_engine.add_record(bad_data_source_code, record_id, record_definition, flags)  # type: ignore[arg-type]


def test_add_record_bad_data_source_code_value(sz_engine: SzEngine) -> None:
    """Test SzEngine().add_record()."""
    bad_data_source_code = "DOESN'T EXIST"
    record_id = "1"
    record_definition: Dict[Any, Any] = {}
    flags = SZ_WITHOUT_INFO
    with pytest.raises(SzBadInputError):
        sz_engine.add_record(bad_data_source_code, record_id, json.dumps(record_definition), flags)


def test_add_record_with_info(sz_engine: SzEngine) -> None:
    """Test SzEngine().add_record_with_info()."""
    data_source_code = "TEST"
    record_id = "1"
    record_definition: Dict[Any, Any] = {}
    flags = SzEngineFlags.SZ_WITH_INFO
    actual = sz_engine.add_record(data_source_code, record_id, json.dumps(record_definition), flags)
    actual_as_dict = json.loads(actual)
    assert schema(add_record_with_info_schema) == actual_as_dict


def test_add_record_bad_record(sz_engine: SzEngine) -> None:
    """Test add_record with bad JSON string."""
    data_source_code = "TEST"
    record_id = "1"
    bad_record_definition = RECORD_STR_BAD
    with pytest.raises(SzError):
        sz_engine.add_record(data_source_code, record_id, bad_record_definition)


def test_add_record_bad_record_id_type(sz_engine: SzEngine) -> None:
    """Test add_record with incorrect record id type."""
    data_source_code = "TEST"
    bad_record_id = 1
    record_definition = RECORD_STR
    with pytest.raises(TypeError):
        sz_engine.add_record(data_source_code, bad_record_id, record_definition)  # type: ignore[arg-type]


def test_add_record_data_source_code_empty(sz_engine: SzEngine) -> None:
    """Test add_record with empty data source code."""
    bad_data_source_code = ""
    record_id = "1"
    record_definition = RECORD_STR
    with pytest.raises(SzError):
        sz_engine.add_record(bad_data_source_code, record_id, record_definition)


def test_add_record_record_str_empty(sz_engine: SzEngine) -> None:
    """Test add_record with empty record as a string"""
    data_source_code = "TEST"
    record_id = "1"
    record_definition = ""
    with pytest.raises(SzError):
        sz_engine.add_record(data_source_code, record_id, record_definition)


# NOTE This doesn't throw an exception because json dumps results in a valid json str '{}'
# def test_add_record_record_dict_empty(sz_engine: SzEngineTest) -> None:
#     """Test add_record with empty record as a dictionary"""
#     with pytest.raises(g2exception.SzError):
#         sz_engine.add_record(data_source_code, record_id, {})


def x_test_add_record_with_info_dict(sz_engine: SzEngine) -> None:
    """Test add_record with flag to return with_info where the record is a dict."""
    data_source_code = "TEST"
    record_id = "1"
    record_definition = RECORD_STR
    flags = SzEngineFlags.SZ_WITH_INFO
    actual = sz_engine.add_record(data_source_code, record_id, record_definition, flags)
    actual_as_dict = json.loads(actual)
    assert schema(add_record_with_info_schema) == actual_as_dict


def test_add_record_with_info_str(sz_engine: SzEngine) -> None:
    """Test add_record with flag to return with_info where the record is a JSON string."""
    data_source_code = "TEST"
    record_id = "1"
    record_definition = RECORD_STR
    flags = SzEngineFlags.SZ_WITH_INFO
    actual = sz_engine.add_record(data_source_code, record_id, record_definition, flags)
    actual_as_dict = json.loads(actual)
    assert schema(add_record_with_info_schema) == actual_as_dict


# TODO: Modify as_python_bytes to convert int to str? More robust and allows mistakes to continue
def test_add_record_with_info_bad_data_source_code_type(
    sz_engine: SzEngine,
) -> None:
    """Test SzEngine().add_record_with_info()."""
    bad_data_source_code = 1
    record_id = "1"
    record_definition: Dict[Any, Any] = {}
    flags = SzEngineFlags.SZ_WITH_INFO
    with pytest.raises(TypeError):
        _ = sz_engine.add_record(bad_data_source_code, record_id, record_definition, flags)  # type: ignore[arg-type]


def test_add_record_with_info_bad_data_source_code_value(
    sz_engine: SzEngine,
) -> None:
    """Test SzEngine().add_record_with_info()."""
    bad_data_source_code = "DOESN'T EXIST"
    record_id = "1"
    record_definition: Dict[Any, Any] = {}
    flags = SzEngineFlags.SZ_WITH_INFO
    with pytest.raises(SzBadInputError):
        _ = sz_engine.add_record(bad_data_source_code, record_id, json.dumps(record_definition), flags)


def test_add_record_with_info_bad_record(sz_engine: SzEngine) -> None:
    """Test add_record with flag to return with_info with bad JSON string."""
    data_source_code = "TEST"
    record_id = "1"
    bad_record_definition = RECORD_STR_BAD
    flags = SzEngineFlags.SZ_WITH_INFO
    with pytest.raises(SzError):
        sz_engine.add_record(data_source_code, record_id, bad_record_definition, flags)


def test_add_record_with_info_bad_record_id_type(sz_engine: SzEngine) -> None:
    """Test add_record with flag to return with_info with incorrect record id type."""
    data_source_code = "TEST"
    bad_record_id = 1
    record_definition = RECORD_DICT
    flags = SzEngineFlags.SZ_WITH_INFO
    with pytest.raises(TypeError):
        sz_engine.add_record(data_source_code, bad_record_id, record_definition, flags)  # type: ignore[arg-type]


def test_add_record_with_info_record_str_empty(sz_engine: SzEngine) -> None:
    """Test add_record_with_info with empty record as a string"""
    data_source_code = "TEST"
    record_id = "1"
    record_definition = ""
    with pytest.raises(SzError):
        sz_engine.add_record(data_source_code, record_id, record_definition)


def test_close_export() -> None:
    """Test SzEngine().close_export()."""
    # TODO: implement.


def test_count_redo_records(sz_engine: SzEngine) -> None:
    """Test SzEngine().count_redo_records()."""
    actual = sz_engine.count_redo_records()
    assert actual > 0


def test_delete_record(sz_engine: SzEngine) -> None:
    """Test SzEngine().delete_record()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    flags = SZ_WITHOUT_INFO
    actual = sz_engine.delete_record(data_source_code, record_id, flags)
    assert actual == ""


def test_delete_record_bad_data_source_code(sz_engine: SzEngine) -> None:
    """Test SzEngine().delete_record()."""
    bad_data_source_code = "XXXX"
    record_id = "9999"
    flags = SZ_WITHOUT_INFO
    with pytest.raises(SzBadInputError):
        sz_engine.delete_record(bad_data_source_code, record_id, flags)


def test_delete_record_bad_record_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().delete_record()."""
    data_source_code = "CUSTOMERS"
    bad_record_id = "9999"
    flags = SZ_WITHOUT_INFO
    actual = sz_engine.delete_record(data_source_code, bad_record_id, flags)
    assert actual == ""


def test_delete_record_with_info(sz_engine: SzEngine) -> None:
    """Test SzEngine().delete_record_with_info()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    flags = SzEngineFlags.SZ_WITH_INFO
    actual = sz_engine.delete_record(data_source_code, record_id, flags)
    actual_as_dict = json.loads(actual)
    assert schema(add_record_with_info_schema) == actual_as_dict


def test_delete_record_with_info_bad_data_source_code(sz_engine: SzEngine) -> None:
    """Test SzEngine().delete_record_with_info()."""
    bad_data_source_code = "XXXX"
    record_id = "9999"
    flags = SzEngineFlags.SZ_WITH_INFO
    with pytest.raises(SzBadInputError):
        _ = sz_engine.delete_record(bad_data_source_code, record_id, flags)


def test_delete_record_with_info_bad_record_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().delete_record_with_info()."""
    data_source_code = "CUSTOMERS"
    bad_record_id = "9999"
    flags = SzEngineFlags.SZ_WITH_INFO
    actual = sz_engine.delete_record(data_source_code, bad_record_id, flags)
    actual_as_dict = json.loads(actual)
    assert schema(add_record_with_info_schema) == actual_as_dict


def test_export_csv_entity_report(sz_engine: SzEngine) -> None:
    """Test SzEngine().export_csv_entity_report()."""
    csv_column_list = "RESOLVED_ENTITY_ID,RESOLVED_ENTITY_NAME,RELATED_ENTITY_ID,MATCH_LEVEL,MATCH_KEY,IS_DISCLOSED,IS_AMBIGUOUS,DATA_SOURCE,RECORD_ID,JSON_DATA"
    flags = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS
    export_handle = sz_engine.export_csv_entity_report(csv_column_list, flags)
    actual = ""
    while True:
        fragment = sz_engine.fetch_next(export_handle)
        if len(fragment) == 0:
            break
        actual += fragment
    sz_engine.close_export(export_handle)
    assert len(actual) > 0


def test_export_json_entity_report(sz_engine: SzEngine) -> None:
    """Test SzEngine().export_json_entity_report()."""
    handle = sz_engine.export_json_entity_report()
    actual = ""
    while True:
        fragment = sz_engine.fetch_next(handle)
        if len(fragment) == 0:
            break
        actual += fragment
    sz_engine.close_export(handle)
    for line in actual.splitlines():
        if len(line) > 0:
            actual_as_dict = json.loads(line)
            assert schema(export_json_entity_report_iterator_schema) == actual_as_dict


def test_fetch_next() -> None:
    """Test SzEngine().fetch_next."""
    # TODO: implement test_fetch_next.


def test_find_interesting_entities_by_entity_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().find_interesting_entities_by_entity_id()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    entity_id = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001")
    flags = SZ_NO_FLAGS
    actual = sz_engine.find_interesting_entities_by_entity_id(entity_id, flags)
    delete_records(sz_engine, test_records)
    if len(actual) > 0:
        actual_as_dict = json.loads(actual)
        assert schema(interesting_entities_schema) == actual_as_dict


def test_find_interesting_entities_by_entity_id_bad_entity_id(
    sz_engine: SzEngine,
) -> None:
    """Test SzEngine().find_interesting_entities_by_entity_id()."""
    bad_entity_id = 0
    flags = SZ_NO_FLAGS
    with pytest.raises(SzNotFoundError):
        _ = sz_engine.find_interesting_entities_by_entity_id(bad_entity_id, flags)


def test_find_interesting_entities_by_record_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().find_interesting_entities_by_record_id()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    flags = SZ_NO_FLAGS
    actual = sz_engine.find_interesting_entities_by_record_id(data_source_code, record_id, flags)
    delete_records(sz_engine, test_records)
    if len(actual) > 0:
        actual_as_dict = json.loads(actual)
        assert schema(interesting_entities_schema) == actual_as_dict


def test_find_interesting_entities_by_record_id_bad_data_source_code(
    sz_engine: SzEngine,
) -> None:
    """Test SzEngine().find_interesting_entities_by_record_id()."""
    bad_data_source_code = "XXXX"
    record_id = "9999"
    flags = SZ_NO_FLAGS
    with pytest.raises(SzUnknownDataSourceError):
        _ = sz_engine.find_interesting_entities_by_record_id(bad_data_source_code, record_id, flags)


def test_find_interesting_entities_by_record_id_bad_record_id(
    sz_engine: SzEngine,
) -> None:
    """Test SzEngine().find_interesting_entities_by_record_id()."""
    data_source_code = "CUSTOMERS"
    bad_record_id = "9999"
    flags = SZ_NO_FLAGS
    with pytest.raises(SzNotFoundError):
        _ = sz_engine.find_interesting_entities_by_record_id(data_source_code, bad_record_id, flags)


def test_find_network_by_entity_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().find_network_by_entity_id()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
        ("CUSTOMERS", "1002"),
    ]
    add_records(sz_engine, test_records)

    entity_ids = [
        get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001"),
        get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1002"),
    ]
    max_degrees = 2
    build_out_degrees = 1
    build_out_max_entities = 10
    flags = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS
    actual = sz_engine.find_network_by_entity_id(
        entity_ids, max_degrees, build_out_degrees, build_out_max_entities, flags
    )
    delete_records(sz_engine, test_records)
    actual_as_dict = json.loads(actual)
    assert schema(network_schema) == actual_as_dict


def test_find_network_by_entity_id_bad_entity_ids(sz_engine: SzEngine) -> None:
    """Test SzEngine().find_network_by_entity_id()."""
    bad_entity_list = [0, 1]
    max_degrees = 2
    build_out_degrees = 1
    max_entities = 10
    flags = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS
    with pytest.raises(SzNotFoundError):
        _ = sz_engine.find_network_by_entity_id(bad_entity_list, max_degrees, build_out_degrees, max_entities, flags)


def test_find_network_by_record_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().find_network_by_record_id()."""
    record_list: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
        ("CUSTOMERS", "1002"),
    ]
    add_records(sz_engine, record_list)
    max_degrees = 2
    build_out_degrees = 1
    max_entities = 10
    flags = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS
    actual = sz_engine.find_network_by_record_id(record_list, max_degrees, build_out_degrees, max_entities, flags)
    delete_records(sz_engine, record_list)
    actual_as_dict = json.loads(actual)
    assert schema(network_schema) == actual_as_dict


def test_find_network_by_record_id_bad_data_source_code(
    sz_engine: SzEngine,
) -> None:
    """Test SzEngine().find_network_by_record_id()."""
    bad_record_list: List[Tuple[str, str]] = [
        ("XXXX", "9999"),
        ("XXXX", "9998"),
    ]
    max_degrees = 2
    build_out_degrees = 1
    max_entities = 10
    flags = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS
    with pytest.raises(SzBadInputError):
        _ = sz_engine.find_network_by_record_id(bad_record_list, max_degrees, build_out_degrees, max_entities, flags)


def test_find_network_by_record_id_bad_record_ids(sz_engine: SzEngine) -> None:
    """Test SzEngine().find_network_by_record_id()."""
    bad_record_list: List[Tuple[str, str]] = [
        ("CUSTOMERS", "9999"),
        ("CUSTOMERS", "9998"),
    ]
    max_degrees = 2
    build_out_degrees = 1
    max_entities = 10
    flags = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS
    with pytest.raises(SzNotFoundError):
        _ = sz_engine.find_network_by_record_id(bad_record_list, max_degrees, build_out_degrees, max_entities, flags)


def test_find_path_by_entity_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().find_path_by_entity_id()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
        ("CUSTOMERS", "1002"),
    ]
    add_records(sz_engine, test_records)
    start_entity_id = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001")
    end_entity_id = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1002")
    max_degrees = 1
    avoid_entity_ids: List[int] = [0]
    required_data_sources: List[str] = ["CUSTOMERS"]
    flags = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS
    actual = sz_engine.find_path_by_entity_id(
        start_entity_id,
        end_entity_id,
        max_degrees,
        avoid_entity_ids,
        required_data_sources,
        flags,
    )
    delete_records(sz_engine, test_records)
    actual_as_dict = json.loads(actual)
    assert schema(path_schema) == actual_as_dict


def test_find_path_by_entity_id_bad_entity_ids(sz_engine: SzEngine) -> None:
    """Test SzEngine().find_path_by_entity_id()."""
    bad_start_entity_id = 0
    bad_end_entity_id = 1
    max_degrees = 1
    avoid_entity_ids: List[int] = [0]
    required_data_sources: List[str] = ["CUSTOMERS"]
    flags = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS
    max_degrees = 1
    with pytest.raises(SzNotFoundError):
        _ = sz_engine.find_path_by_entity_id(
            bad_start_entity_id,
            bad_end_entity_id,
            max_degrees,
            avoid_entity_ids,
            required_data_sources,
            flags,
        )


def test_find_path_by_record_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().find_path_by_record_id()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
        ("CUSTOMERS", "1002"),
    ]
    add_records(sz_engine, test_records)
    start_data_source_code = "CUSTOMERS"
    start_record_id = "1001"
    end_data_source_code = "CUSTOMERS"
    end_record_id = "1002"
    max_degrees = 1
    avoid_record_keys: List[Tuple[str, str]] = [("CUSTOMERS", "0000")]
    required_data_sources: List[str] = ["CUSTOMERS"]
    flags = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS
    actual = sz_engine.find_path_by_record_id(
        start_data_source_code,
        start_record_id,
        end_data_source_code,
        end_record_id,
        max_degrees,
        avoid_record_keys,
        required_data_sources,
        flags,
    )
    delete_records(sz_engine, test_records)
    actual_as_dict = json.loads(actual)
    assert schema(path_schema) == actual_as_dict


def test_find_path_by_record_id_bad_data_source_code(sz_engine: SzEngine) -> None:
    """Test SzEngine().find_path_by_record_id()."""
    bad_start_data_source_code = "XXXX"
    start_record_id = "9999"
    bad_end_data_source_code = "XXXX"
    end_record_id = "9998"
    max_degrees = 1
    avoid_record_keys: List[Tuple[str, str]] = [("CUSTOMERS", "0000")]
    required_data_sources: List[str] = ["CUSTOMERS"]
    flags = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS
    with pytest.raises(SzBadInputError):
        _ = sz_engine.find_path_by_record_id(
            bad_start_data_source_code,
            start_record_id,
            bad_end_data_source_code,
            end_record_id,
            max_degrees,
            avoid_record_keys,
            required_data_sources,
            flags,
        )


def test_find_path_by_record_id_bad_record_ids(sz_engine: SzEngine) -> None:
    """Test SzEngine().find_path_by_record_id()."""
    start_data_source_code = "CUSTOMERS"
    bad_start_record_id = "9999"
    end_data_source_code = "CUSTOMERS"
    bad_end_record_id = "9998"
    max_degrees = 1
    avoid_record_keys: List[Tuple[str, str]] = [("CUSTOMERS", "0000")]
    required_data_sources: List[str] = ["CUSTOMERS"]
    flags = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS
    with pytest.raises(SzNotFoundError):
        _ = sz_engine.find_path_by_record_id(
            start_data_source_code,
            bad_start_record_id,
            end_data_source_code,
            bad_end_record_id,
            max_degrees,
            avoid_record_keys,
            required_data_sources,
            flags,
        )


def test_get_active_config_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().get_active_config_id()."""
    actual = sz_engine.get_active_config_id()
    assert actual >= 0


def test_get_entity_by_entity_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().get_entity_by_entity_id()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
        ("CUSTOMERS", "1002"),
    ]
    add_records(sz_engine, test_records)
    entity_id = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001")
    flags = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS
    actual = sz_engine.get_entity_by_entity_id(entity_id, flags)
    delete_records(sz_engine, test_records)
    actual_as_dict = json.loads(actual)
    assert schema(resolved_entity_schema) == actual_as_dict


def test_get_entity_by_record_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().get_entity_by_record_id()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    flags = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS
    actual = sz_engine.get_entity_by_record_id(data_source_code, record_id, flags)
    delete_records(sz_engine, test_records)
    actual_as_dict = json.loads(actual)
    assert schema(resolved_entity_schema) == actual_as_dict


def test_get_entity_by_record_id_bad_data_source_code(sz_engine: SzEngine) -> None:
    """Test SzEngine().get_entity_by_record_id()."""
    bad_data_source_code = "XXXX"
    record_id = "9999"
    flags = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS
    with pytest.raises(SzBadInputError):
        _ = sz_engine.get_entity_by_record_id(bad_data_source_code, record_id, flags)


def test_get_entity_by_record_id_bad_record_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().get_entity_by_record_id()."""
    data_source_code = "CUSTOMERS"
    bad_record_id = "9999"
    flags = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS
    with pytest.raises(SzNotFoundError):
        _ = sz_engine.get_entity_by_record_id(data_source_code, bad_record_id, flags)


def test_get_record(sz_engine: SzEngine) -> None:
    """Test SzEngine().get_record()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    flags = SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS
    actual = sz_engine.get_record(data_source_code, record_id, flags)
    delete_records(sz_engine, test_records)
    actual_as_dict = json.loads(actual)
    assert schema(record_schema) == actual_as_dict


def test_get_record_bad_data_source_code(sz_engine: SzEngine) -> None:
    """Test SzEngine().get_record()."""
    bad_data_source_code = "XXXX"
    record_id = "9999"
    flags = SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS
    with pytest.raises(SzBadInputError):
        _ = sz_engine.get_record(bad_data_source_code, record_id, flags)


def test_get_record_bad_record_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().get_record()."""
    data_source_code = "CUSTOMERS"
    bad_record_id = "9999"
    flags = SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS
    with pytest.raises(SzNotFoundError):
        _ = sz_engine.get_record(data_source_code, bad_record_id, flags)


def test_get_redo_record(sz_engine: SzEngine) -> None:
    """Test SzEngine().get_redo_record()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
        ("CUSTOMERS", "1002"),
        ("CUSTOMERS", "1003"),
    ]
    add_records(sz_engine, test_records)
    actual = sz_engine.get_redo_record()
    delete_records(sz_engine, test_records)
    actual_as_dict = json.loads(actual)
    assert schema(redo_record_schema) == actual_as_dict


def test_get_stats(sz_engine: SzEngine) -> None:
    """Test SzEngine().stats()."""
    actual = sz_engine.get_stats()
    actual_as_dict = json.loads(actual)
    assert schema(stats_schema) == actual_as_dict


def test_get_virtual_entity_by_record_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().get_virtual_entity_by_record_id()."""
    record_list: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
        ("CUSTOMERS", "1002"),
    ]
    add_records(sz_engine, record_list)
    flags = SzEngineFlags.SZ_VIRTUAL_ENTITY_DEFAULT_FLAGS
    actual = sz_engine.get_virtual_entity_by_record_id(record_list, flags)
    delete_records(sz_engine, record_list)
    actual_as_dict = json.loads(actual)
    assert schema(virtual_entity_schema) == actual_as_dict


def test_get_virtual_entity_by_record_id_bad_data_source_code(
    sz_engine: SzEngine,
) -> None:
    """Test SzEngine().get_virtual_entity_by_record_id()."""
    bad_record_list: List[Tuple[str, str]] = [
        ("XXXX", "9999"),
        ("XXXX", "9998"),
    ]
    flags = SzEngineFlags.SZ_VIRTUAL_ENTITY_DEFAULT_FLAGS
    with pytest.raises(SzBadInputError):
        _ = sz_engine.get_virtual_entity_by_record_id(bad_record_list, flags)


def test_get_virtual_entity_by_record_id_bad_record_ids(
    sz_engine: SzEngine,
) -> None:
    """Test SzEngine().get_virtual_entity_by_record_id()."""
    bad_record_list: List[Tuple[str, str]] = [
        ("CUSTOMERS", "9999"),
        ("CUSTOMERS", "9998"),
    ]
    flags = SzEngineFlags.SZ_VIRTUAL_ENTITY_DEFAULT_FLAGS
    with pytest.raises(SzNotFoundError):
        _ = sz_engine.get_virtual_entity_by_record_id(bad_record_list, flags)


def test_how_entity_by_entity_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().how_entity_by_entity_id()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    entity_id = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001")
    flags = SzEngineFlags.SZ_HOW_ENTITY_DEFAULT_FLAGS
    actual = sz_engine.how_entity_by_entity_id(entity_id, flags)
    delete_records(sz_engine, test_records)
    actual_as_dict = json.loads(actual)
    assert schema(how_results_schema) == actual_as_dict


def test_how_entity_by_entity_id_bad_entity_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().how_entity_by_entity_id()."""
    bad_entity_id = 0
    flags = SzEngineFlags.SZ_HOW_ENTITY_DEFAULT_FLAGS
    with pytest.raises(SzNotFoundError):
        _ = sz_engine.how_entity_by_entity_id(bad_entity_id, flags)


def test_preprocess_record(sz_engine: SzEngine) -> None:
    """Test SzEngine().preprocess_record()."""
    record_definition: str = DATA_SOURCES.get("CUSTOMERS", {}).get("1001", {}).get("Json", {})
    flags = SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS
    actual = sz_engine.preprocess_record(record_definition, flags)
    actual_as_dict = json.loads(actual)
    assert schema(preprocess_record_schema) == actual_as_dict


# TODO This needs fixing first: https://senzing.atlassian.net/browse/GDEV-3924?atlOrigin=eyJpIjoiYjY2OWNkOTc5ZDRiNDgzYmE5ZjE2NjIzOTZiYmNjNTgiLCJwIjoiaiJ9
# def test_preprocess_record_bad_record(sz_engine: SzEngineTest) -> None:
#     """Test SzEngine().preprocess_record()."""
#     record_definition: str = (
#         '"RECORD_TYPE": "PERSON", "PRIMARY_NAME_LAST": "Smith", "PRIMARY_NAME_FIRST": "Robert", "DATE_OF_BIRTH": "12/11/1978"}'
#     )
#     with pytest.raises(SzBadInputError):
#         sz_engine.preprocess_record(record_definition)


def test_prime_engine(sz_engine: SzEngine) -> None:
    """Test SzEngine().prime_engine()."""
    sz_engine.prime_engine()


def test_reevaluate_entity(sz_engine: SzEngine) -> None:
    """Test SzEngine().get_entity_id_from_record_id()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    entity_id = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001")
    flags = SZ_WITHOUT_INFO
    actual = sz_engine.reevaluate_entity(entity_id, flags)
    delete_records(sz_engine, test_records)
    assert actual == ""


def test_reevaluate_entity_bad_entity_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().get_entity_id_from_record_id()."""
    bad_entity_id = 0
    flags = SZ_WITHOUT_INFO
    actual = sz_engine.reevaluate_entity(bad_entity_id, flags)
    assert actual == ""


def test_reevaluate_entity_with_info(sz_engine: SzEngine) -> None:
    """Test SzEngine().reevaluate_entity_with_info()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    entity_id = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001")
    flags = SzEngineFlags.SZ_WITH_INFO
    actual = sz_engine.reevaluate_entity(entity_id, flags)
    delete_records(sz_engine, test_records)
    actual_as_dict = json.loads(actual)
    assert schema(add_record_with_info_schema_fixme) == actual_as_dict


def test_reevaluate_entity_with_info_bad_entity_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().reevaluate_entity_with_info()."""
    bad_entity_id = 0
    flags = SzEngineFlags.SZ_WITH_INFO
    _ = sz_engine.reevaluate_entity(bad_entity_id, flags)


def test_reevaluate_record(sz_engine: SzEngine) -> None:
    """Test SzEngine().get_entity_id_from_record_id()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    flags = SZ_WITHOUT_INFO
    actual = sz_engine.reevaluate_record(data_source_code, record_id, flags)
    delete_records(sz_engine, test_records)
    assert actual == ""


def test_reevaluate_record_bad_data_source_code(sz_engine: SzEngine) -> None:
    """Test SzEngine().reevaluate_record()."""
    bad_data_source_code = "XXXX"
    record_id = "9999"
    flags = SZ_WITHOUT_INFO
    with pytest.raises(SzBadInputError):
        sz_engine.reevaluate_record(bad_data_source_code, record_id, flags)


def test_reevaluate_record_bad_record_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().reevaluate_record()."""
    data_source_code = "CUSTOMERS"
    bad_record_id = "9999"
    flags = SZ_WITHOUT_INFO
    actual = sz_engine.reevaluate_record(data_source_code, bad_record_id, flags)
    assert actual == ""


# TODO: Fix test after GDEV-3790
# with pytest.raises(SzNotFoundError):
#     sz_engine.reevaluate_record(data_source_code, bad_record_id, flags)


def test_reevaluate_record_with_info(sz_engine: SzEngine) -> None:
    """Test SzEngine().reevaluate_entity_with_info()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    flags = SzEngineFlags.SZ_WITH_INFO
    actual = sz_engine.reevaluate_record(data_source_code, record_id, flags)
    delete_records(sz_engine, test_records)
    actual_as_dict = json.loads(actual)
    assert schema(add_record_with_info_schema) == actual_as_dict


def test_reevaluate_record_with_info_bad_data_source_code(
    sz_engine: SzEngine,
) -> None:
    """Test SzEngine().reevaluate_entity_with_info()."""
    bad_data_source_code = "XXXX"
    record_id = "9999"
    flags = SzEngineFlags.SZ_WITH_INFO
    with pytest.raises(SzBadInputError):
        _ = sz_engine.reevaluate_record(bad_data_source_code, record_id, flags)


def test_reevaluate_record_with_info_bad_record_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().reevaluate_entity_with_info()."""
    data_source_code = "CUSTOMERS"
    bad_record_id = "9999"
    flags = SzEngineFlags.SZ_WITH_INFO
    sz_engine.reevaluate_record(data_source_code, bad_record_id, flags)
    # TODO: Fix test after GDEV-3790
    # with pytest.raises(SzNotFoundError):
    #     _ = sz_engine.reevaluate_record(data_source_code, bad_record_id, flags)


def test_search_by_attributes(sz_engine: SzEngine) -> None:
    """Test SzEngine().search_by_attributes
    ()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
        ("CUSTOMERS", "1002"),
        ("CUSTOMERS", "1003"),
    ]
    add_records(sz_engine, test_records)
    attributes = json.dumps({"NAME_FULL": "BOB SMITH", "EMAIL_ADDRESS": "bsmith@work.com"})
    search_profile = ""
    flags = SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS
    actual = sz_engine.search_by_attributes(attributes, flags, search_profile)
    delete_records(sz_engine, test_records)
    if len(actual) > 0:
        actual_as_dict = json.loads(actual)
        assert schema(search_schema) == actual_as_dict


def test_search_by_attributes_bad_attributes(sz_engine: SzEngine) -> None:
    """Test SzEngine().search_by_attributes()."""
    bad_attributes = "{"
    search_profile = ""
    flags = SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS
    with pytest.raises(SzError):
        _ = sz_engine.search_by_attributes(bad_attributes, flags, search_profile)


def test_why_entities(sz_engine: SzEngine) -> None:
    """Test SzEngine().why_entities()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
        ("CUSTOMERS", "1002"),
    ]
    add_records(sz_engine, test_records)
    entity_id_1 = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001")
    entity_id_2 = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1002")
    flags = SzEngineFlags.SZ_WHY_ENTITIES_DEFAULT_FLAGS
    actual = sz_engine.why_entities(entity_id_1, entity_id_2, flags)
    delete_records(sz_engine, test_records)
    actual_as_dict = json.loads(actual)
    assert schema(why_entities_results_schema) == actual_as_dict


def test_why_entities_bad_entity_ids(sz_engine: SzEngine) -> None:
    """Test SzEngine().why_entities()."""
    bad_entity_id_1 = 0
    entity_id_2 = 1
    flags = SzEngineFlags.SZ_WHY_ENTITIES_DEFAULT_FLAGS
    with pytest.raises(SzNotFoundError):
        _ = sz_engine.why_entities(bad_entity_id_1, entity_id_2, flags)


def test_why_record_in_entity() -> None:
    """Test SzEngine().why_record_in_entity()."""
    # TODO: implement.


def test_why_records(sz_engine: SzEngine) -> None:
    """Test SzEngine().why_records()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
        ("CUSTOMERS", "1002"),
    ]
    add_records(sz_engine, test_records)
    data_source_code_1 = "CUSTOMERS"
    record_id_1 = "1001"
    data_source_code_2 = "CUSTOMERS"
    record_id_2 = "1002"
    flags = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS
    actual = sz_engine.why_records(data_source_code_1, record_id_1, data_source_code_2, record_id_2, flags)
    delete_records(sz_engine, test_records)
    actual_as_dict = json.loads(actual)
    assert schema(why_entity_results_schema) == actual_as_dict


def test_why_records_bad_data_source_code(sz_engine: SzEngine) -> None:
    """Test SzEngine().why_records()."""
    data_source_code_1 = "CUSTOMERS"
    record_id_1 = "1001"
    bad_data_source_code_2 = "XXXX"
    record_id_2 = "9999"
    flags = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS
    with pytest.raises(SzBadInputError):
        _ = sz_engine.why_records(data_source_code_1, record_id_1, bad_data_source_code_2, record_id_2, flags)


def test_why_records_bad_record_id(sz_engine: SzEngine) -> None:
    """Test SzEngine().why_records()."""
    data_source_code_1 = "CUSTOMERS"
    record_id_1 = "1001"
    data_source_code_2 = "CUSTOMERS"
    bad_record_id_2 = "9999"
    flags = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS
    with pytest.raises(SzNotFoundError):
        _ = sz_engine.why_records(data_source_code_1, record_id_1, data_source_code_2, bad_record_id_2, flags)


# -----------------------------------------------------------------------------
# Unique testcases
# -----------------------------------------------------------------------------


def test_add_record_str(sz_engine: SzEngine) -> None:
    """Test add_record where the record is a JSON string."""
    data_source_code = "TEST"
    record_id = "1"
    json_data = RECORD_STR
    actual = sz_engine.add_record(data_source_code, record_id, json_data)
    assert actual == ""


# TODO: Modify as_python_bytes to convert int to str? More robust and allows mistakes to continue
# TODO: Uncomment testcase after Senzing code build 2024_05_01__07_22.
# def test_add_record_bad_data_source_code_type(sz_engine: SzEngineTest) -> None:
#     """Test add_record with incorrect data source code type."""
#     data_source_code = 1
#     record_id = "1"
#     json_data = RECORD_DICT
#     with pytest.raises(TypeError):
#         sz_engine.add_record(data_source_code, record_id, json_data)


# TODO: Uncomment testcase after Senzing code build 2024_05_01__07_22.
# def test_add_record_bad_data_source_code_value(sz_engine: SzEngineTest) -> None:
#     """Test add_record with non-existent data source code."""
#     data_source_code = "DOESN'T EXIST"
#     record_id = "1"
#     json_data = RECORD_DICT
#     with pytest.raises(SzError):
#         sz_engine.add_record(data_source_code, record_id, json_data)

# def test_add_record_dict(sz_engine: SzEngineTest) -> None:
#     """Test add_record where the record is a dict."""
#     data_source_code = "TEST"
#     record_id = "1"
#     json_data = RECORD_DICT
#     sz_engine.add_record(data_source_code, record_id, json_data)


# def test_add_truthset_data(engine_vars: Dict[Any, Any]) -> None:
#     """Add truthset data for tests"""
#     sz_engine = SzEngineTest()
#     sz_engine._initialize(  # pylint: disable=W0212
#         engine_vars["INSTANCE_NAME"],
#         engine_vars["SETTINGS"],
#         engine_vars["VERBOSE_LOGGING"],
#     )
#     add_records_truthset(sz_engine)


def test_constructor(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    actual = SzEngineCore(
        instance_name=engine_vars["INSTANCE_NAME"],
        settings=engine_vars["SETTINGS"],
        verbose_logging=engine_vars["VERBOSE_LOGGING"],
    )
    assert isinstance(actual, SzEngine)


# def test_constructor_bad_instance_name(engine_vars: Dict[Any, Any]) -> None:
#     """Test constructor."""
#     bad_instance_name = ""
#     with pytest.raises(SzError):
#         test_object = SzEngineTest()
#         test_object._initialize(  # pylint: disable=W0212
#             bad_instance_name,
#             engine_vars["SETTINGS"],
#         )


# def test_constructor_bad_settings(engine_vars: Dict[Any, Any]) -> None:
#     """Test constructor."""
#     bad_settings = ""
#     with pytest.raises(SzError):
#         test_object = SzEngineTest()
#         test_object._initialize(  # pylint: disable=W0212
#             engine_vars["INSTANCE_NAME"],
#             bad_settings,
#         )


# TODO: Was having issues with the as_c_ini in init
# def test_constructor_bad_verbose_logging(engine_vars: Dict[Any, Any]):
#     """Test constructor."""


# def test_initialize_bad_config_id(engine_vars: Dict[Any, Any]) -> None:
#     """Test init_with_config_id with non-existent config id."""
#     instance_name = engine_vars["INSTANCE_NAME"]
#     settings = engine_vars["SETTINGS"]
#     config_id = 0
#     sz_engine = SzEngineTest()
#     sz_engine.initialize(instance_name, settings, config_id)


def test_constructor_dict(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    actual = SzEngineCore()
    actual.initialize(  # pylint: disable=W0212
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS_DICT"],
    )
    assert isinstance(actual, SzEngine)


def test_destroy(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    actual = SzEngineCore()
    actual.initialize(  # pylint: disable=W0212
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    actual._destroy()


def test_exception(sz_engine: SzEngineCore) -> None:
    """Test exceptions."""
    with pytest.raises(Exception):
        sz_engine.check_result(-1)


def test_reinitialize(sz_engine: SzEngineCore) -> None:
    """Test SzEngine().reinitialize()."""
    config_id = sz_engine.get_active_config_id()
    sz_engine._reinitialize(config_id)  # pylint: disable=W0212


def test_reinitialize_bad_config_id(sz_engine: SzEngineCore) -> None:
    """Test SzEngine().reinitialize()."""
    bad_default_config_id = "string"
    with pytest.raises(TypeError):
        sz_engine._reinitialize(bad_default_config_id)  # type: ignore[arg-type]


def test_reinitialize_missing_config_id(sz_engine: SzEngineCore) -> None:
    """Test SzDiagnostic().reinit() raising error."""
    with pytest.raises(SzError):
        sz_engine._reinitialize(999)


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------


def add_records(sz_engine: SzEngine, record_id_list: List[Tuple[str, str]]) -> None:
    """Add all of the records in the list."""
    flags = SZ_WITHOUT_INFO
    for record_identification in record_id_list:
        datasource = record_identification[0]
        record_id = record_identification[1]
        record = DATA_SOURCES.get(datasource, {}).get(record_id, {})
        actual = sz_engine.add_record(
            record.get("DataSource", ""),
            record.get("Id", ""),
            record.get("Json", ""),
            flags,
        )
        assert actual == ""


def add_records_truthset(sz_engine: SzEngine, do_redo: bool = True) -> None:
    """Add all truth-set the records."""
    flags = SZ_WITHOUT_INFO
    for record_set in DATA_SOURCES.values():
        for record in record_set.values():
            actual = sz_engine.add_record(
                record.get("DataSource"),
                record.get("Id"),
                record.get("Json"),
                flags,
            )
            assert actual == ""
    if do_redo:
        while sz_engine.count_redo_records() > 0:
            redo_record = sz_engine.get_redo_record()
            actual = sz_engine.process_redo_record(redo_record, flags)
            assert actual == ""


def delete_records(sz_engine: SzEngine, record_id_list: List[Tuple[str, str]]) -> None:
    """Delete all of the records in the list."""
    flags = SZ_WITHOUT_INFO
    for record_identification in record_id_list:
        datasource = record_identification[0]
        record_id = record_identification[1]
        record = DATA_SOURCES.get(datasource, {}).get(record_id, {})
        actual = sz_engine.delete_record(record.get("DataSource", ""), record.get("Id", ""), flags)
        assert actual == ""


def delete_records_truthset(sz_engine: SzEngine) -> None:
    """Delete all truth-set the records."""
    flags = SZ_WITHOUT_INFO
    for record_set in DATA_SOURCES.values():
        for record in record_set.values():
            actual = sz_engine.delete_record(record.get("DataSource"), record.get("Id"), flags)
            assert actual == ""


def get_entity_id_from_record_id(sz_engine: SzEngine, data_source_code: str, record_id: str) -> int:
    """Given a (datasource, record_id), return the entity ID."""
    entity = sz_engine.get_entity_by_record_id(data_source_code, record_id)
    entity_as_dict = json.loads(entity)
    return int(entity_as_dict.get("RESOLVED_ENTITY", {}).get("ENTITY_ID", 0))


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="sz_config", scope="function")
def szconfig_fixture(engine_vars: Dict[Any, Any]) -> SzConfig:
    """
    Single szconfig object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    result = SzConfigCore()
    result.initialize(  # pylint: disable=W0212
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    return result


@pytest.fixture(name="sz_configmanager", scope="function")
def szconfigmanager_fixture(engine_vars: Dict[Any, Any]) -> SzConfigManager:
    """
    Single szconfigmanager object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    result = SzConfigManagerCore()
    result.initialize(  # pylint: disable=W0212
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    return result


@pytest.fixture(name="sz_engine", scope="function")
def szengine_fixture(engine_vars: Dict[Any, Any]) -> SzEngine:
    """
    Single SzEngine object to use for all tests.
    engine_vars is returned from conftest.py.
    """

    result = SzEngineCore()
    result.initialize(  # pylint: disable=W0212
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    return result


# -----------------------------------------------------------------------------
# Schemas
# -----------------------------------------------------------------------------

add_record_with_info_schema = {
    "DATA_SOURCE": str,
    "RECORD_ID": str,
    "AFFECTED_ENTITIES": [{"ENTITY_ID": int}],
}

add_record_with_info_schema_fixme = {
    "AFFECTED_ENTITIES": [{"ENTITY_ID": int}],
}

export_json_entity_report_iterator_schema = {
    "RESOLVED_ENTITY": {
        "ENTITY_ID": int,
        Optional("ENTITY_NAME"): str,
        Optional("FEATURES"): {},
        Optional("RECORDS"): [
            {
                "DATA_SOURCE": str,
                "RECORD_ID": str,
                Optional("ENTITY_TYPE"): str,
                "INTERNAL_ID": int,
                Optional("ENTITY_KEY"): str,
                Optional("ENTITY_DESC"): str,
                "MATCH_KEY": str,
                Optional("MATCH_LEVEL"): int,
                "MATCH_LEVEL_CODE": str,
                "ERRULE_CODE": str,
                Optional("LAST_SEEN_DT"): str,
            }
        ],
    },
    Optional("RELATED_ENTITIES"): [
        {
            "ENTITY_ID": int,
            "MATCH_LEVEL_CODE": str,
            "MATCH_KEY": str,
            "ERRULE_CODE": str,
            "IS_DISCLOSED": int,
            "IS_AMBIGUOUS": int,
            "ENTITY_NAME": str,
            "RECORD_SUMMARY": [{"DATA_SOURCE": str, "RECORD_COUNT": int}],
        }
    ],
}


g2_config_schema = {
    "G2_CONFIG": {
        Optional("CFG_ETYPE"): [
            {
                "ETYPE_ID": int,
                "ETYPE_CODE": str,
                "ETYPE_DESC": str,
            },
        ],
        "CFG_DSRC_INTEREST": [],
        "CFG_RCLASS": [
            {
                "RCLASS_ID": int,
                "RCLASS_CODE": str,
                "RCLASS_DESC": str,
                "IS_DISCLOSED": str,
            },
        ],
        "CFG_FTYPE": [
            {
                "FTYPE_ID": int,
                "FTYPE_CODE": Or(str, None),
                "FCLASS_ID": int,
                "FTYPE_FREQ": str,
                "FTYPE_EXCL": str,
                "FTYPE_STAB": str,
                "PERSIST_HISTORY": str,
                "USED_FOR_CAND": str,
                "DERIVED": str,
                "RTYPE_ID": int,
                "ANONYMIZE": str,
                "VERSION": int,
                "SHOW_IN_MATCH_KEY": str,
            },
        ],
        "CFG_FCLASS": [
            {
                "FCLASS_ID": int,
                "FCLASS_CODE": str,
            },
        ],
        "CFG_FBOM": [
            {
                "FTYPE_ID": int,
                Optional("FELEM_ID"): int,
                Optional("EXEC_ORDER"): int,
                "DISPLAY_LEVEL": int,
                "DISPLAY_DELIM": Or(str, None),
                "DERIVED": str,
            },
        ],
        "CFG_FELEM": [
            {
                Optional("FELEM_ID"): int,
                "FELEM_CODE": str,
                Optional("TOKENIZE"): str,
                "DATA_TYPE": str,
            },
        ],
        "CFG_DSRC": [
            {
                "DSRC_ID": int,
                "DSRC_CODE": str,
                "DSRC_DESC": str,
                Optional("DSRC_RELY"): int,
                "RETENTION_LEVEL": str,
                Optional("CONVERSATIONAL"): str,
            },
        ],
        "CFG_EFBOM": [
            {
                "EFCALL_ID": int,
                "FTYPE_ID": int,
                Optional("FELEM_ID"): int,
                Optional("EXEC_ORDER"): int,
                "FELEM_REQ": str,
            },
        ],
        "CFG_EFUNC": [
            {
                "EFUNC_ID": int,
                "EFUNC_CODE": str,
                Optional("FUNC_LIB"): str,
                Optional("FUNC_VER"): str,
                "CONNECT_STR": str,
                "LANGUAGE": Or(str, None),
            },
        ],
        "CFG_EFCALL": [
            {
                "EFCALL_ID": int,
                "FTYPE_ID": int,
                Optional("FELEM_ID"): int,
                "EFUNC_ID": int,
                Optional("EXEC_ORDER"): int,
                "EFEAT_FTYPE_ID": int,
                "IS_VIRTUAL": str,
            },
        ],
        "CFG_SFCALL": [
            {
                "SFCALL_ID": int,
                "FTYPE_ID": int,
                Optional("FELEM_ID"): int,
                "SFUNC_ID": int,
                Optional("EXEC_ORDER"): int,
            },
        ],
        "CFG_SFUNC": [
            {
                "SFUNC_ID": int,
                "SFUNC_CODE": str,
                Optional("FUNC_LIB"): str,
                Optional("FUNC_VER"): str,
                "CONNECT_STR": str,
                "LANGUAGE": Or(str, None),
            },
        ],
        "SYS_OOM": [
            {
                "OOM_TYPE": str,
                "OOM_LEVEL": str,
                "FTYPE_ID": int,
                "THRESH1_CNT": int,
                "THRESH1_OOM": int,
                "NEXT_THRESH": int,
            },
        ],
        "CFG_CFUNC": [
            {
                "CFUNC_ID": int,
                "CFUNC_CODE": str,
                Optional("FUNC_LIB"): str,
                Optional("FUNC_VER"): str,
                "CONNECT_STR": str,
                "ANON_SUPPORT": str,
                "LANGUAGE": Or(str, None),
            },
        ],
        "CFG_CFCALL": [
            {
                "CFCALL_ID": int,
                "FTYPE_ID": int,
                "CFUNC_ID": int,
                Optional("EXEC_ORDER"): int,
            },
        ],
        "CFG_GPLAN": [
            {
                "GPLAN_ID": int,
                "GPLAN_CODE": str,
            },
        ],
        "CFG_ERRULE": [
            {
                "ERRULE_ID": int,
                "ERRULE_CODE": str,
                Optional("ERRULE_DESC"): str,
                "RESOLVE": str,
                "RELATE": str,
                Optional("REF_SCORE"): int,
                "RTYPE_ID": int,
                "QUAL_ERFRAG_CODE": str,
                "DISQ_ERFRAG_CODE": Or(str, None),
                "ERRULE_TIER": Or(int, None),
            },
        ],
        "CFG_ERFRAG": [
            {
                "ERFRAG_ID": int,
                "ERFRAG_CODE": str,
                "ERFRAG_DESC": str,
                "ERFRAG_SOURCE": str,
                "ERFRAG_DEPENDS": Or(str, None),
            },
        ],
        "CFG_CFBOM": [
            {
                "CFCALL_ID": int,
                "FTYPE_ID": int,
                Optional("FELEM_ID"): int,
                Optional("EXEC_ORDER"): int,
            },
        ],
        "CFG_DFUNC": [
            {
                "DFUNC_ID": int,
                "DFUNC_CODE": str,
                Optional("FUNC_LIB"): str,
                Optional("FUNC_VER"): str,
                "CONNECT_STR": str,
                "ANON_SUPPORT": str,
                "LANGUAGE": Or(str, None),
            },
        ],
        "CFG_DFCALL": [
            {
                "DFCALL_ID": int,
                "FTYPE_ID": int,
                "DFUNC_ID": int,
                Optional("EXEC_ORDER"): int,
            },
        ],
        "CFG_DFBOM": [
            {
                "DFCALL_ID": int,
                "FTYPE_ID": int,
                Optional("FELEM_ID"): int,
                Optional("EXEC_ORDER"): int,
            },
        ],
        "CFG_CFRTN": [
            {
                "CFRTN_ID": int,
                "CFUNC_ID": int,
                "FTYPE_ID": int,
                "CFUNC_RTNVAL": str,
                Optional("EXEC_ORDER"): int,
                "SAME_SCORE": int,
                "CLOSE_SCORE": int,
                "LIKELY_SCORE": int,
                "PLAUSIBLE_SCORE": int,
                "UN_LIKELY_SCORE": int,
            },
        ],
        "CFG_RTYPE": [
            {
                "RTYPE_ID": int,
                "RTYPE_CODE": str,
                "RCLASS_ID": int,
                Optional("REL_STRENGTH"): int,
                "BREAK_RES": str,
            },
        ],
        "CFG_GENERIC_THRESHOLD": [
            {
                "GPLAN_ID": int,
                "BEHAVIOR": str,
                "FTYPE_ID": int,
                "CANDIDATE_CAP": int,
                "SCORING_CAP": int,
                "SEND_TO_REDO": str,
            },
        ],
        "CFG_FBOVR": [
            {
                "FTYPE_ID": int,
                "UTYPE_CODE": str,
                "FTYPE_FREQ": str,
                "FTYPE_EXCL": str,
                "FTYPE_STAB": str,
            },
        ],
        "CFG_ATTR": [
            {
                "ATTR_ID": int,
                "ATTR_CODE": str,
                "ATTR_CLASS": str,
                "FTYPE_CODE": Or(str, None),
                "FELEM_CODE": Or(str, None),
                "FELEM_REQ": str,
                "DEFAULT_VALUE": Or(str, None),
                Optional("ADVANCED"): str,
                "INTERNAL": Or(str, None),
            },
        ],
        "CONFIG_BASE_VERSION": {
            "VERSION": str,
            "BUILD_VERSION": str,
            "BUILD_DATE": str,
            "BUILD_NUMBER": str,
            "COMPATIBILITY_VERSION": {
                "CONFIG_VERSION": str,
            },
        },
    },
}

how_results_schema = {
    "HOW_RESULTS": {
        "RESOLUTION_STEPS": [{}],
        "FINAL_STATE": {
            "NEED_REEVALUATION": int,
            "VIRTUAL_ENTITIES": [
                {
                    "VIRTUAL_ENTITY_ID": str,
                    "MEMBER_RECORDS": [
                        {
                            "INTERNAL_ID": int,
                            Optional("RECORDS"): [{"DATA_SOURCE": str, "RECORD_ID": str}],
                        }
                    ],
                }
            ],
        },
    }
}

interesting_entities_schema: Dict[Any, Any] = {
    "INTERESTING_ENTITIES": {"ENTITIES": []},
}

network_schema = {
    "ENTITY_PATHS": [],
    "ENTITIES": [
        {
            "RESOLVED_ENTITY": {
                "ENTITY_ID": int,
                Optional("ENTITY_NAME"): str,
                Optional("RECORD_SUMMARY"): [
                    {
                        "DATA_SOURCE": str,
                        "RECORD_COUNT": int,
                        Optional("FIRST_SEEN_DT"): str,
                        Optional("LAST_SEEN_DT"): str,
                    }
                ],
                Optional("LAST_SEEN_DT"): str,
            },
            Optional("RELATED_ENTITIES"): [
                {
                    "ENTITY_ID": int,
                    "MATCH_LEVEL_CODE": str,
                    "MATCH_KEY": str,
                    "ERRULE_CODE": str,
                    "IS_DISCLOSED": int,
                    "IS_AMBIGUOUS": int,
                    "ENTITY_NAME": str,
                    "RECORD_SUMMARY": [{"DATA_SOURCE": str, "RECORD_COUNT": int}],
                }
            ],
        }
    ],
}

path_schema = {
    "ENTITY_PATHS": [{"START_ENTITY_ID": int, "END_ENTITY_ID": int, "ENTITIES": [int]}],
    "ENTITIES": [
        {
            "RESOLVED_ENTITY": {
                "ENTITY_ID": int,
                Optional("ENTITY_NAME"): str,
                Optional("RECORD_SUMMARY"): [
                    {
                        "DATA_SOURCE": str,
                        "RECORD_COUNT": int,
                        Optional("FIRST_SEEN_DT"): str,
                        Optional("LAST_SEEN_DT"): str,
                    }
                ],
                Optional("LAST_SEEN_DT"): str,
            },
            Optional("RELATED_ENTITIES"): [
                {
                    "ENTITY_ID": int,
                    "MATCH_LEVEL_CODE": str,
                    "MATCH_KEY": str,
                    "ERRULE_CODE": str,
                    "IS_DISCLOSED": int,
                    "IS_AMBIGUOUS": int,
                    "ENTITY_NAME": str,
                    "RECORD_SUMMARY": [{"DATA_SOURCE": str, "RECORD_COUNT": int}],
                }
            ],
        }
    ],
}

preprocess_record_schema = {
    "JSON_DATA": {str: str},
    Optional("FEATURES"): {},
    Optional("UNMAPPED_DATA"): {},
}

process_withinfo_schema = {
    "DATA_SOURCE": str,
    "RECORD_ID": str,
    "AFFECTED_ENTITIES": [{"ENTITY_ID": int}],
    "INTERESTING_ENTITIES": {"ENTITIES": []},
}

record_schema = {"DATA_SOURCE": str, "RECORD_ID": str, "JSON_DATA": {}}

redo_record_schema = {
    "REASON": str,
    "DATA_SOURCE": str,
    "RECORD_ID": str,
    Optional("ENTITY_TYPE"): str,
    "DSRC_ACTION": str,
}

resolved_entity_schema = {
    "RESOLVED_ENTITY": {
        "ENTITY_ID": int,
        Optional("ENTITY_NAME"): str,
        Optional("FEATURES"): {},
        Optional("RECORD_SUMMARY"): [
            {
                "DATA_SOURCE": str,
                "RECORD_COUNT": int,
                Optional("FIRST_SEEN_DT"): str,
                Optional("LAST_SEEN_DT"): str,
            }
        ],
        Optional("LAST_SEEN_DT"): str,
        Optional("RECORDS"): [
            {
                "DATA_SOURCE": str,
                "RECORD_ID": str,
                Optional("ENTITY_TYPE"): str,
                "INTERNAL_ID": int,
                Optional("ENTITY_KEY"): str,
                Optional("ENTITY_DESC"): str,
                "MATCH_KEY": str,
                Optional("MATCH_LEVEL"): int,
                "MATCH_LEVEL_CODE": str,
                "ERRULE_CODE": str,
                Optional("LAST_SEEN_DT"): str,
            },
        ],
    },
    Optional("RELATED_ENTITIES"): [
        {
            "ENTITY_ID": int,
            "MATCH_LEVEL_CODE": str,
            "MATCH_KEY": str,
            "ERRULE_CODE": str,
            "IS_DISCLOSED": int,
            "IS_AMBIGUOUS": int,
            "ENTITY_NAME": str,
            "RECORD_SUMMARY": [{"DATA_SOURCE": str, "RECORD_COUNT": int}],
        }
    ],
}

search_schema = {
    "RESOLVED_ENTITIES": [
        {
            "MATCH_INFO": {
                Optional("MATCH_LEVEL"): int,
                "MATCH_LEVEL_CODE": str,
                "MATCH_KEY": str,
                "ERRULE_CODE": str,
                "FEATURE_SCORES": {},
            },
            "ENTITY": {
                "RESOLVED_ENTITY": {
                    "ENTITY_ID": int,
                    Optional("ENTITY_NAME"): str,
                    Optional("FEATURES"): {},
                    Optional("RECORD_SUMMARY"): [
                        {
                            "DATA_SOURCE": str,
                            "RECORD_COUNT": int,
                            Optional("FIRST_SEEN_DT"): str,
                            Optional("LAST_SEEN_DT"): str,
                        }
                    ],
                    Optional("LAST_SEEN_DT"): str,
                }
            },
        }
    ]
}

stats_schema = {
    "workload": {
        "apiVersion": str,
        "loadedRecords": int,
        "addedRecords": int,
        "bulkAddedRecords": int,
        "optimizedOut": int,
        "optimizedOutSkipped": int,
        "newObsEnt": int,
        "obsEntHashSame": int,
        "obsEntHashDiff": int,
        "partiallyResolved": int,
        "deletedRecords": int,
        "changeDeletes": int,
        "reevaluations": int,
        "repairedEntities": int,
        "duration": int,
        "retries": int,
        "candidates": int,
        "actualAmbiguousTest": int,
        "cachedAmbiguousTest": int,
        "libFeatCacheHit": int,
        "libFeatCacheMiss": int,
        "resFeatStatCacheHit": int,
        "resFeatStatCacheMiss": int,
        "libFeatInsert": int,
        "resFeatStatInsert": int,
        "resFeatStatUpdateAttempt": int,
        "resFeatStatUpdateFail": int,
        Optional("resFeatStatUpdate"): int,
        "unresolveTest": int,
        "abortedUnresolve": int,
        "lockWaits": {},
        "unresolveTriggers": {},
        "reresolveTriggers": {},
        "reresolveSkipped": int,
        "filteredObsFeat": int,
        "expressedFeatureCalls": [{}],
        "expressedFeaturesCreated": [{}],
        "scoredPairs": [{}],
        "cacheHit": [{}],
        "cacheMiss": [{}],
        "redoTriggers": [{}],
        "latchContention": [],
        "highContentionFeat": [],
        "highContentionResEnt": [{}],
        "genericDetect": [],
        "candidateBuilders": [{}],
        "suppressedCandidateBuilders": [],
        "suppressedScoredFeatureType": [],
        Optional("reducedScoredFeatureType"): [],
        "suppressedCandidateBuildersForReresolve": [],
        "suppressedScoredFeatureTypeForReresolve": [],
        "suppressedDisclosedRelationshipDomainCount": int,
        "corruptEntityTestDiagnosis": {},
        "threadState": {},
        "systemResources": {},
    }
}

virtual_entity_schema = {
    "RESOLVED_ENTITY": {
        "ENTITY_ID": int,
        Optional("ENTITY_NAME"): str,
        Optional("FEATURES"): {},
        Optional("RECORD_SUMMARY"): [
            {
                "DATA_SOURCE": str,
                "RECORD_COUNT": int,
                Optional("FIRST_SEEN_DT"): str,
                Optional("LAST_SEEN_DT"): str,
            }
        ],
        Optional("LAST_SEEN_DT"): str,
        Optional("RECORDS"): [
            {
                "DATA_SOURCE": str,
                "RECORD_ID": str,
                Optional("ENTITY_TYPE"): str,
                "INTERNAL_ID": int,
                Optional("ENTITY_KEY"): str,
                Optional("ENTITY_DESC"): str,
                Optional("LAST_SEEN_DT"): str,
                Optional("FEATURES"): [{"LIB_FEAT_ID": int}],
            },
        ],
    },
}

why_entities_results_schema = {
    "WHY_RESULTS": [
        {
            "ENTITY_ID": int,
            "ENTITY_ID_2": int,
            "MATCH_INFO": {},
        }
    ],
    "ENTITIES": [
        {
            "RESOLVED_ENTITY": {
                "ENTITY_ID": int,
                Optional("ENTITY_NAME"): str,
                Optional("FEATURES"): {},
                Optional("RECORD_SUMMARY"): [{}],
                Optional("LAST_SEEN_DT"): str,
                Optional("RECORDS"): [
                    {
                        "DATA_SOURCE": str,
                        "RECORD_ID": str,
                        Optional("ENTITY_TYPE"): str,
                        "INTERNAL_ID": int,
                        Optional("ENTITY_KEY"): str,
                        Optional("ENTITY_DESC"): str,
                        "MATCH_KEY": str,
                        Optional("MATCH_LEVEL"): int,
                        "MATCH_LEVEL_CODE": str,
                        "ERRULE_CODE": str,
                        Optional("LAST_SEEN_DT"): str,
                        Optional("FEATURES"): [{}],
                    }
                ],
            },
            Optional("RELATED_ENTITIES"): [
                {
                    "ENTITY_ID": int,
                    "MATCH_LEVEL_CODE": str,
                    "MATCH_KEY": str,
                    "ERRULE_CODE": str,
                    "IS_DISCLOSED": int,
                    "IS_AMBIGUOUS": int,
                    "ENTITY_NAME": str,
                    "RECORD_SUMMARY": [{"DATA_SOURCE": str, "RECORD_COUNT": int}],
                }
            ],
        }
    ],
}


why_entity_results_schema = {
    "WHY_RESULTS": [
        {
            "INTERNAL_ID": int,
            "ENTITY_ID": int,
            "FOCUS_RECORDS": [{}],
            "MATCH_INFO": {
                "WHY_KEY": str,
                "WHY_ERRULE_CODE": str,
                "MATCH_LEVEL_CODE": str,
                "CANDIDATE_KEYS": {},
                "FEATURE_SCORES": {},
            },
        }
    ],
    "ENTITIES": [
        {
            "RESOLVED_ENTITY": {
                "ENTITY_ID": int,
                Optional("ENTITY_NAME"): str,
                Optional("FEATURES"): {},
                Optional("RECORD_SUMMARY"): [{}],
                Optional("LAST_SEEN_DT"): str,
                Optional("RECORDS"): [
                    {
                        "DATA_SOURCE": str,
                        "RECORD_ID": str,
                        Optional("ENTITY_TYPE"): str,
                        "INTERNAL_ID": int,
                        Optional("ENTITY_KEY"): str,
                        Optional("ENTITY_DESC"): str,
                        "MATCH_KEY": str,
                        Optional("MATCH_LEVEL"): int,
                        "MATCH_LEVEL_CODE": str,
                        "ERRULE_CODE": str,
                        Optional("LAST_SEEN_DT"): str,
                        Optional("FEATURES"): [{}],
                    }
                ],
            },
            Optional("RELATED_ENTITIES"): [
                {
                    "ENTITY_ID": int,
                    "MATCH_LEVEL_CODE": str,
                    "MATCH_KEY": str,
                    "ERRULE_CODE": str,
                    "IS_DISCLOSED": int,
                    "IS_AMBIGUOUS": int,
                    "ENTITY_NAME": str,
                    "RECORD_SUMMARY": [{"DATA_SOURCE": str, "RECORD_COUNT": int}],
                }
            ],
        }
    ],
}
