# TODO Check and change the exception type with raises to more specific exception instead of g2exception
# TODO Add tests for flags
# TODO Think about and test how to make the g2helper conversions more robust and possibly raise g2exception
# TODO Test calling delete record again
# TODO Add tests for incorrect ini parms paths and incorrect DB details for constructor
# TODO value/type tests and handling ctype exceptions from g2helpers - needs thought
import json
from typing import Any, Dict, List, Tuple

import pytest
from pytest_schema import Or, schema
from senzing_truthset import (
    TRUTHSET_CUSTOMER_RECORDS,
    TRUTHSET_DATASOURCES,
    TRUTHSET_REFERENCE_RECORDS,
    TRUTHSET_WATCHLIST_RECORDS,
)

from senzing import (
    SzConfigurationError,
    SzEngineFlags,
    SzError,
    SzUnknownDataSourceError,
    szconfig,
    szconfigmanager,
    szengine,
)

# -----------------------------------------------------------------------------
# SzEngine pre tests
# -----------------------------------------------------------------------------


# def test_exception(sz_engine: szengine.SzEngine):
#     """Test exceptions."""
#     actual = sz_engine.new_exception(0)
#     assert isinstance(actual, Exception)


def test_constructor(engine_vars) -> None:
    """Test constructor."""
    actual = szengine.SzEngine(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
        engine_vars["VERBOSE_LOGGING"],
    )
    assert isinstance(actual, szengine.SzEngine)


def test_constructor_bad_module_name(engine_vars) -> None:
    """Test constructor."""
    bad_module_name = ""
    with pytest.raises(SzError):
        szengine.SzEngine(
            bad_module_name,
            engine_vars["SETTINGS"],
        )


def test_constructor_bad_ini_params(engine_vars) -> None:
    """Test constructor."""
    bad_ini_params = ""
    with pytest.raises(SzError):
        szengine.SzEngine(
            engine_vars["INSTANCE_NAME"],
            bad_ini_params,
        )


# TODO Was having issues with the as_c_ini in init
# def test_constructor_bad_verbose_logging(engine_vars):
#     """Test constructor."""


def test_add_truthset_datasources(
    sz_engine: szengine.SzEngine,
    sz_configmanager: szconfigmanager.SzConfigManager,
    sz_config: szconfig.SzConfig,
) -> None:
    """Add needed datasources for tests."""
    config_handle = sz_config.create_config()
    for data_source_code in TRUTHSET_DATASOURCES.keys():
        sz_config.add_data_source(config_handle, data_source_code)
    config_definition = sz_config.export_config(config_handle)
    config_id = sz_configmanager.add_config(config_definition, "Test")
    sz_configmanager.set_default_config_id(config_id)
    sz_engine.reinitialize(config_id)


# TODO Doesn't appear to be working, pointing at wrong G2C I think
# def test_add_truthset_data(engine_vars):
#     """Add truthset data for tests"""
#     sz_engine = szengine.SzEngine(
#         engine_vars["INSTANCE_NAME"],
#         engine_vars["SETTINGS"],
#         engine_vars["VERBOSE_LOGGING"],
#     )
#     add_records_truthset(sz_engine: szengine.SzEngine)


# -----------------------------------------------------------------------------
# SzEngine testcases
# -----------------------------------------------------------------------------


# TODO:  Figure out why SRD_EXCEPTION
# def test_add_record_dict(sz_engine: szengine.SzEngine):
#     """Test add_record where the record is a dict."""
#     data_source_code = "TEST"
#     record_id = "1"
#     json_data = RECORD_DICT
#     sz_engine.add_record(data_source_code, record_id, json_data)


# TODO:  Figure out why SRD_EXCEPTION
# def test_add_record_str(sz_engine: szengine.SzEngine):
#     """Test add_record where the record is a JSON string."""
#     data_source_code = "TEST"
#     record_id = "1"
#     json_data = RECORD_STR
#     sz_engine.add_record(data_source_code, record_id, json_data)


# TODO Modify as_c_char_p to convert int to str? More robust and allows mistakes to continue
# TODO:  Figure out why SRD_EXCEPTION
# def test_add_record_bad_data_source_code_type(sz_engine: szengine.SzEngine):
#     """Test add_record with incorrect data source code type."""
#     data_source_code = 1
#     record_id = "1"
#     json_data = RECORD_DICT
#     with pytest.raises(TypeError):
#         sz_engine.add_record(data_source_code, record_id, json_data)

# TODO:  Figure out why SRD_EXCEPTION
# def test_add_record_bad_data_source_code_value(sz_engine: szengine.SzEngine):
#     """Test add_record with non-existent data source code."""
#     data_source_code = "DOESN'T EXIST"
#     record_id = "1"
#     json_data = RECORD_DICT
#     with pytest.raises(SzError):
#         sz_engine.add_record(data_source_code, record_id, json_data)


def test_add_record(sz_engine: szengine.SzEngine) -> None:
    """Test SzEngine().add_record()."""
    data_source_code = "TEST"
    record_id = "1"
    record_definition: Dict[Any, Any] = {}
    flags = SzEngineFlags.SZ_WITHOUT_INFO
    sz_engine.add_record(data_source_code, record_id, record_definition, flags)


def test_add_record_bad_data_source_code_type(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test SzEngine().add_record()."""
    bad_data_source_code = 1
    record_id = "1"
    record_definition: Dict[Any, Any] = {}
    flags = SzEngineFlags.SZ_WITHOUT_INFO
    with pytest.raises(TypeError):
        sz_engine.add_record(
            bad_data_source_code, record_id, record_definition, flags  # type: ignore[arg-type]
        )


def test_add_record_bad_data_source_code_value(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test SzEngine().add_record()."""
    bad_data_source_code = "DOESN'T EXIST"
    record_id = "1"
    record_definition: Dict[Any, Any] = {}
    flags = SzEngineFlags.SZ_WITHOUT_INFO
    with pytest.raises(SzUnknownDataSourceError):
        sz_engine.add_record(bad_data_source_code, record_id, record_definition, flags)


def test_add_record_with_info(sz_engine: szengine.SzEngine) -> None:
    """Test SzEngine().add_record_with_info()."""
    data_source_code = "TEST"
    record_id = "1"
    record_definition: Dict[Any, Any] = {}
    flags = SzEngineFlags.SZ_WITH_INFO
    actual = sz_engine.add_record(data_source_code, record_id, record_definition, flags)
    actual_dict = json.loads(actual)
    assert schema(add_record_with_info_schema) == actual_dict


def test_add_record_bad_record(sz_engine: szengine.SzEngine) -> None:
    """Test add_record with bad JSON string."""
    data_source_code = "TEST"
    record_id = "1"
    bad_record_definition = RECORD_STR_BAD
    with pytest.raises(SzError):
        sz_engine.add_record(data_source_code, record_id, bad_record_definition)


def test_add_record_bad_record_id_type(sz_engine: szengine.SzEngine) -> None:
    """Test add_record with incorrect record id type."""
    data_source_code = "TEST"
    bad_record_id = 1
    record_definition = RECORD_DICT
    with pytest.raises(TypeError):
        sz_engine.add_record(data_source_code, bad_record_id, record_definition)  # type: ignore[arg-type]


def test_add_record_data_source_code_empty(sz_engine: szengine.SzEngine) -> None:
    """Test add_record with empty data source code."""
    bad_data_source_code = ""
    record_id = "1"
    record_definition = RECORD_DICT
    with pytest.raises(SzError):
        sz_engine.add_record(bad_data_source_code, record_id, record_definition)


def test_add_record_record_str_empty(sz_engine: szengine.SzEngine) -> None:
    """Test add_record with empty record as a string"""
    data_source_code = "TEST"
    record_id = "1"
    record_definition = ""
    with pytest.raises(SzError):
        sz_engine.add_record(data_source_code, record_id, record_definition)


# NOTE This doesn't throw an exception because json dumps results in a valid json str '{}'
# def test_add_record_record_dict_empty(sz_engine: szengine.SzEngine):
#     """Test add_record with empty record as a dictionary"""
#     with pytest.raises(g2exception.SzError):
#         sz_engine.add_record(data_source_code, record_id, {})


def test_add_record_with_info_dict(sz_engine: szengine.SzEngine) -> None:
    """Test add_record with flag to return with_info where the record is a dict."""
    data_source_code = "TEST"
    record_id = "1"
    record_definition = RECORD_DICT
    flags = SzEngineFlags.SZ_WITH_INFO
    actual = sz_engine.add_record(data_source_code, record_id, record_definition, flags)
    actual_dict = json.loads(actual)
    assert schema(add_record_with_info_schema) == actual_dict


def test_add_record_with_info_str(sz_engine: szengine.SzEngine) -> None:
    """Test add_record with flag to return with_info where the record is a JSON string."""
    data_source_code = "TEST"
    record_id = "1"
    record_definition = RECORD_STR
    flags = SzEngineFlags.SZ_WITH_INFO
    actual = sz_engine.add_record(data_source_code, record_id, record_definition, flags)
    actual_dict = json.loads(actual)
    assert schema(add_record_with_info_schema) == actual_dict


# TODO Modify as_c_char_p to convert int to str? More robust and allows mistakes to continue
def test_add_record_with_info_bad_data_source_code_type(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test add_record with flag to return with_info with incorrect data source code type."""
    bad_data_source_code = 1
    record_id = "1"
    record_definition = RECORD_DICT
    flags = SzEngineFlags.SZ_WITH_INFO
    with pytest.raises(TypeError):
        sz_engine.add_record(bad_data_source_code, record_id, record_definition, flags)  # type: ignore[arg-type]


def test_add_record_with_info_bad_data_source_code_value(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test add_record with flag to return with_info with non-existent data source code."""
    bad_data_source_code = "DOESN'T EXIST"
    record_id = "1"
    record_definition = RECORD_DICT
    flags = SzEngineFlags.SZ_WITH_INFO
    with pytest.raises(SzError):
        _ = sz_engine.add_record(
            bad_data_source_code, record_id, record_definition, flags
        )


def test_add_record_with_info_bad_record(sz_engine: szengine.SzEngine) -> None:
    """Test add_record with flag to return with_info with bad JSON string."""
    data_source_code = "TEST"
    record_id = "1"
    bad_record_definition = RECORD_STR_BAD
    flags = SzEngineFlags.SZ_WITH_INFO
    with pytest.raises(SzError):
        sz_engine.add_record(data_source_code, record_id, bad_record_definition, flags)


def test_add_record_with_info_bad_record_id_type(sz_engine: szengine.SzEngine) -> None:
    """Test add_record with flag to return with_info with incorrect record id type."""
    data_source_code = "TEST"
    bad_record_id = 1
    record_definition = RECORD_DICT
    flags = SzEngineFlags.SZ_WITH_INFO
    with pytest.raises(TypeError):
        sz_engine.add_record(data_source_code, bad_record_id, record_definition, flags)  # type: ignore[arg-type]


def test_add_record_with_info_record_str_empty(sz_engine: szengine.SzEngine) -> None:
    """Test add_record_with_info with empty record as a string"""
    data_source_code = "TEST"
    record_id = "1"
    record_definition = ""
    with pytest.raises(SzError):
        sz_engine.add_record(data_source_code, record_id, record_definition)


def test_close_export() -> None:
    """Test SzEngine().close_export()."""
    # TODO: implement.


def test_count_redo_records(sz_engine: szengine.SzEngine) -> None:
    """Test count_redo_records"""
    actual = sz_engine.count_redo_records()
    assert actual == 0


def test_delete_record(sz_engine: szengine.SzEngine) -> None:
    """Test delete_record."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    flags = SzEngineFlags.SZ_WITHOUT_INFO
    sz_engine.delete_record(data_source_code, record_id, flags)


def test_delete_record_bad_data_source_code(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test SzEngine().delete_record()."""
    bad_data_source_code = "XXXX"
    record_id = "9999"
    flags = SzEngineFlags.SZ_WITHOUT_INFO
    with pytest.raises(SzConfigurationError):
        sz_engine.delete_record(bad_data_source_code, record_id, flags)


def test_delete_record_bad_record_id(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test SzEngine().delete_record()."""
    data_source_code = "CUSTOMERS"
    bad_record_id = "9999"
    flags = SzEngineFlags.SZ_WITHOUT_INFO
    sz_engine.delete_record(data_source_code, bad_record_id, flags)


def test_delete_record_with_info(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test SzEngine().delete_record_with_info()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    flags = SzEngineFlags.SZ_WITH_INFO
    actual = sz_engine.delete_record(data_source_code, record_id, flags)
    actual_dict = json.loads(actual)
    assert schema(add_record_with_info_schema) == actual_dict


def test_delete_record_with_info_bad_data_source_code(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test SzEngine().delete_record_with_info()."""
    bad_data_source_code = "XXXX"
    record_id = "9999"
    flags = SzEngineFlags.SZ_WITH_INFO
    with pytest.raises(SzConfigurationError):
        _ = sz_engine.delete_record(bad_data_source_code, record_id, flags)


def test_delete_record_with_info_bad_record_id(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test SzEngine().delete_record_with_info()."""
    data_source_code = "CUSTOMERS"
    bad_record_id = "9999"
    flags = SzEngineFlags.SZ_WITH_INFO
    actual = sz_engine.delete_record(data_source_code, bad_record_id, flags)
    actual_dict = json.loads(actual)
    assert schema(add_record_with_info_schema) == actual_dict


def test_export_csv_entity_report(sz_engine: szengine.SzEngine) -> None:
    """Test export_csv_entity_report."""
    csv_headers = "RESOLVED_ENTITY_ID,RESOLVED_ENTITY_NAME,RELATED_ENTITY_ID,MATCH_LEVEL,MATCH_KEY,IS_DISCLOSED,IS_AMBIGUOUS,DATA_SOURCE,RECORD_ID,JSON_DATA,LAST_SEEN_DT,NAME_DATA,ATTRIBUTE_DATA,IDENTIFIER_DATA,ADDRESS_DATA,PHONE_DATA,RELATIONSHIP_DATA,ENTITY_DATA,OTHER_DATA"
    flags = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS
    export_handle = sz_engine.export_csv_entity_report(csv_headers, flags)
    actual = ""
    while True:
        fragment = sz_engine.fetch_next(export_handle)
        if not fragment:
            break
        actual += fragment
    sz_engine.close_export(export_handle)
    assert len(actual) > 0


def test_export_csv_entity_report_bad_header(sz_engine: szengine.SzEngine) -> None:
    """Test export_csv_entity_report with incorrect header value."""
    bad_csv_headers = "RESOLVED_ENTITY_,RESOLVED_ENTITY_NAME,RELATED_ENTITY_ID,MATCH_LEVEL,MATCH_KEY,IS_DISCLOSED,IS_AMBIGUOUS,DATA_SOURCE,RECORD_ID,JSON_DATA,LAST_SEEN_DT,NAME_DATA,ATTRIBUTE_DATA,IDENTIFIER_DATA,ADDRESS_DATA,PHONE_DATA,RELATIONSHIP_DATA,ENTITY_DATA,OTHER_DATA"
    with pytest.raises(SzError):
        sz_engine.export_csv_entity_report(bad_csv_headers)


def test_export_json_entity_report(sz_engine: szengine.SzEngine) -> None:
    """Test export_json_entity_report."""
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
            actual_dict = json.loads(line)
            assert schema(export_json_entity_report_iterator_schema) == actual_dict


def test_fetch_next() -> None:
    """Test SzEngine().fetch_next."""
    # TODO: implement test_fetch_next.


def test_find_interesting_entities_by_entity_id(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test SzEngine().find_interesting_entities_by_entity_id()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    entity_id = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001")
    flags = SzEngineFlags.SZ_NO_FLAGS
    actual = sz_engine.find_interesting_entities_by_entity_id(entity_id, flags)
    delete_records(sz_engine, test_records)
    if len(actual) > 0:
        actual_dict = json.loads(actual)
        assert schema(interesting_entities_schema) == actual_dict


def test_find_interesting_entities_by_entity_id_bad_entity_id(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test SzEngine().find_interesting_entities_by_entity_id()."""
    bad_entity_id = 0
    flags = SzEngineFlags.SZ_NO_FLAGS
    # TODO: Fix test when C code works
    # with pytest.raises(SzNotFoundError):
    #     _ = sz_engine.find_interesting_entities_by_entity_id(bad_entity_id, flags)


def test_find_interesting_entities_by_record_id(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test SzEngine().find_interesting_entities_by_record_id()."""
    test_records: List[Tuple[str, str]] = [
        ("CUSTOMERS", "1001"),
    ]
    add_records(sz_engine, test_records)
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    flags = SzEngineFlags.SZ_NO_FLAGS
    actual = sz_engine.find_interesting_entities_by_record_id(
        data_source_code, record_id, flags
    )
    delete_records(sz_engine, test_records)
    if len(actual) > 0:
        actual_dict = json.loads(actual)
        assert schema(interesting_entities_schema) == actual_dict


def test_find_interesting_entities_by_record_id_bad_data_source_code(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test SzEngine().find_interesting_entities_by_record_id()."""
    bad_data_source_code = "XXXX"
    record_id = "9999"
    flags = SzEngineFlags.SZ_NO_FLAGS
    sz_engine.find_interesting_entities_by_record_id(
        bad_data_source_code, record_id, flags
    )
    # TODO: Fix test
    # with pytest.raises(SzUnknownDataSourceError):
    #     _ = sz_engine.find_interesting_entities_by_record_id(
    #         bad_data_source_code, record_id, flags
    #     )


def test_find_interesting_entities_by_record_id_bad_record_id(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test SzEngine().find_interesting_entities_by_record_id()."""
    data_source_code = "CUSTOMERS"
    bad_record_id = "9999"
    flags = SzEngineFlags.SZ_NO_FLAGS
    sz_engine.find_interesting_entities_by_record_id(
        data_source_code, bad_record_id, flags
    )
    # TODO: Fix test
    # with pytest.raises(SzNotFoundError):
    #     _ = sz_engine.find_interesting_entities_by_record_id(
    #         data_source_code, bad_record_id, flags
    #     )


def test_find_network_by_entity_id_list_as_dict(sz_engine: szengine.SzEngine) -> None:
    """Test find_network_by_entity_id with entity_list as a dict"""
    entity_id_1 = get_entity_id_from_record_id(sz_engine, "WATCHLIST", "1027")
    entity_id_2 = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1069")
    entity_list = {
        "ENTITIES": [
            {"ENTITY_ID": entity_id_1},
            {"ENTITY_ID": entity_id_2},
        ]
    }
    max_degree = 5
    build_out_degree = 2
    max_entities = 10
    actual = sz_engine.find_network_by_entity_id(
        entity_list, max_degree, build_out_degree, max_entities
    )
    actual_dict = json.loads(actual)
    assert schema(network_schema) == actual_dict


def test_find_network_by_entity_id_list_as_str(sz_engine: szengine.SzEngine) -> None:
    """Test find_network_by_entity_id with entity_list as a string."""
    entity_id_1 = get_entity_id_from_record_id(sz_engine, "WATCHLIST", "1027")
    entity_id_2 = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1069")
    entity_list = (
        f'{{"ENTITIES": [{{"ENTITY_ID": {entity_id_1}}}, {{"ENTITY_ID":'
        f" {entity_id_2}}}]}}"
    )
    max_degree = 5
    build_out_degree = 2
    max_entities = 10
    actual = sz_engine.find_network_by_entity_id(
        entity_list, max_degree, build_out_degree, max_entities
    )
    actual_dict = json.loads(actual)
    assert schema(network_schema) == actual_dict


def test_find_network_by_entity_id_bad_entity_ids(sz_engine: szengine.SzEngine) -> None:
    """Test find_network_by_entity_id with non-existent entities."""
    entity_list = {
        "ENTITIES": [
            {"ENTITY_ID": 99999999999998},
            {"ENTITY_ID": 99999999999999},
        ]
    }
    max_degree = 5
    build_out_degree = 2
    max_entities = 10
    with pytest.raises(SzError):
        sz_engine.find_network_by_entity_id(
            entity_list, max_degree, build_out_degree, max_entities
        )


def test_find_network_by_entity_id_empty_entity_list(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test find_network_by_entity_id with empty list."""
    entity_list = {}
    max_degree = 5
    build_out_degree = 2
    max_entities = 10
    actual = sz_engine.find_network_by_entity_id(
        entity_list, max_degree, build_out_degree, max_entities
    )
    actual_dict = json.loads(actual)
    assert schema(network_schema) == actual_dict


def test_find_network_by_entity_id_return_dict_type(sz_engine: szengine.SzEngine):
    """Test find_network_by_entity_id_return_dict returns a dict"""
    entity_id_1 = get_entity_id_from_record_id(sz_engine, "WATCHLIST", "1027")
    entity_id_2 = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1069")
    entity_list = {
        "ENTITIES": [
            {"ENTITY_ID": entity_id_1},
            {"ENTITY_ID": entity_id_2},
        ]
    }
    max_degree = 5
    build_out_degree = 2
    max_entities = 10
    actual = sz_engine.find_network_by_entity_id_return_dict(
        entity_list, max_degree, build_out_degree, max_entities
    )
    assert isinstance(actual, dict)


def test_find_network_by_record_id_list_as_dict(sz_engine: szengine.SzEngine) -> None:
    """Test find_network_by_record_id with record_list as a dict."""
    record_list = {
        "RECORDS": [
            {"DATA_SOURCE": "WATCHLIST", "RECORD_ID": "1027"},
            {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1069"},
        ]
    }
    max_degree = 5
    build_out_degree = 2
    max_entities = 10
    actual = sz_engine.find_network_by_record_id(
        record_list, max_degree, build_out_degree, max_entities
    )
    actual_dict = json.loads(actual)
    assert schema(network_schema) == actual_dict


def test_find_network_by_record_id_list_as_str(sz_engine: szengine.SzEngine) -> None:
    """Test find_network_by_record_id with record_list as a string."""
    record_list = (
        '{"RECORDS": [{"DATA_SOURCE": "WATCHLIST", "RECORD_ID": "1027"},'
        ' {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1069"}]}'
    )
    max_degree = 5
    build_out_degree = 2
    max_entities = 10
    actual = sz_engine.find_network_by_record_id(
        record_list, max_degree, build_out_degree, max_entities
    )
    actual_dict = json.loads(actual)
    assert schema(network_schema) == actual_dict


def test_find_network_by_record_id_bad_data_source_code(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test find_network_by_record_id with non-existent data source."""
    record_list = {
        "RECORDS": [
            {"DATA_SOURCE": "DOESN'T EXIST", "RECORD_ID": "1027"},
            {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1069"},
        ]
    }
    max_degree = 5
    build_out_degree = 2
    max_entities = 10
    with pytest.raises(SzError):
        sz_engine.find_network_by_record_id(
            record_list, max_degree, build_out_degree, max_entities
        )


def test_find_network_by_record_id_bad_record_ids(sz_engine: szengine.SzEngine) -> None:
    """Test find_network_by_record_id with non-existent record id."""
    record_list = {
        "RECORDS": [
            {"DATA_SOURCE": "WATCHLIST", "RECORD_ID": "9999999999999999"},
            {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1069"},
        ]
    }
    max_degree = 5
    build_out_degree = 2
    max_entities = 10
    with pytest.raises(SzError):
        sz_engine.find_network_by_record_id(
            record_list, max_degree, build_out_degree, max_entities
        )


def test_find_network_by_record_id_empty_record_list(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test find_network_by_record_id with empty list."""
    record_list = {}
    max_degree = 5
    build_out_degree = 2
    max_entities = 10
    actual = sz_engine.find_network_by_record_id(
        record_list, max_degree, build_out_degree, max_entities
    )
    actual_dict = json.loads(actual)
    assert schema(network_schema) == actual_dict


def test_find_network_by_record_id_return_dict_type(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test find_network_by_record_id_return_dict returns a dict"""
    record_list = {
        "RECORDS": [
            {"DATA_SOURCE": "WATCHLIST", "RECORD_ID": "1027"},
            {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1069"},
        ]
    }
    max_degree = 5
    build_out_degree = 2
    max_entities = 10
    actual = sz_engine.find_network_by_record_id_return_dict(
        record_list, max_degree, build_out_degree, max_entities
    )
    assert isinstance(actual, dict)


def test_find_path_by_entity_id(sz_engine: szengine.SzEngine) -> None:
    """Test find_path_by_entity_id."""
    entity_id_1 = get_entity_id_from_record_id(sz_engine, "WATCHLIST", "2082")
    entity_id_2 = get_entity_id_from_record_id(sz_engine, "REFERENCE", "2131")
    max_degree = 5
    actual = sz_engine.find_path_by_entity_id(entity_id_1, entity_id_2, max_degree)
    actual_dict = json.loads(actual)
    assert schema(path_schema) == actual_dict


def test_find_path_by_entity_id_bad_entity_ids(sz_engine: szengine.SzEngine) -> None:
    """Test find_path_by_entity_id with non-existent entities."""
    entity_id_1 = 99999999999998
    entity_id_2 = 99999999999999
    max_degree = 5
    with pytest.raises(SzError):
        sz_engine.find_path_by_entity_id(entity_id_1, entity_id_2, max_degree)


def test_find_path_by_entity_id_return_dict_type(sz_engine: szengine.SzEngine) -> None:
    """Test find_path_by_entity_id_return_dict returns a dict"""
    entity_id_1 = get_entity_id_from_record_id(sz_engine, "WATCHLIST", "2082")
    entity_id_2 = get_entity_id_from_record_id(sz_engine, "REFERENCE", "2131")
    max_degree = 5
    actual = sz_engine.find_path_by_entity_id_return_dict(
        entity_id_1, entity_id_2, max_degree
    )
    assert isinstance(actual, dict)


def test_find_path_by_record_id(sz_engine: szengine.SzEngine) -> None:
    """Test find_path_by_record_id."""
    data_source_code_1 = "REFERENCE"
    record_id_1 = "2081"
    data_source_code_2 = "REFERENCE"
    record_id_2 = "2132"
    max_degree = 5
    actual = sz_engine.find_path_by_record_id(
        data_source_code_1, record_id_1, data_source_code_2, record_id_2, max_degree
    )
    actual_dict = json.loads(actual)
    assert schema(path_schema) == actual_dict


def test_find_path_by_record_id_bad_data_source_code(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test find_path_by_record_id with non-existent data source."""
    data_source_code_1 = "DOESN'T EXIST"
    record_id_1 = "2081"
    data_source_code_2 = "REFERENCE"
    record_id_2 = "2132"
    max_degree = 5
    with pytest.raises(SzError):
        sz_engine.find_path_by_record_id(
            data_source_code_1, record_id_1, data_source_code_2, record_id_2, max_degree
        )


def test_find_path_by_record_id_bad_record_ids(sz_engine: szengine.SzEngine) -> None:
    """Test find_path_by_record_id with non-existent record id."""
    data_source_code_1 = "REFERENCE"
    record_id_1 = "9999999999999999"
    data_source_code_2 = "REFERENCE"
    record_id_2 = "2132"
    max_degree = 5
    with pytest.raises(SzError):
        sz_engine.find_path_by_record_id(
            data_source_code_1, record_id_1, data_source_code_2, record_id_2, max_degree
        )


def test_find_path_by_record_id_return_dict_type(sz_engine: szengine.SzEngine) -> None:
    """Test find_path_by_record_id_return_dict returns a dict"""
    data_source_code_1 = "REFERENCE"
    record_id_1 = "2081"
    data_source_code_2 = "REFERENCE"
    record_id_2 = "2132"
    max_degree = 5
    actual = sz_engine.find_path_by_record_id_return_dict(
        data_source_code_1, record_id_1, data_source_code_2, record_id_2, max_degree
    )
    assert isinstance(actual, dict)


def test_find_path_including_source_by_entity_id_excluded_entities_empty(
    sz_engine,
) -> None:
    """Test find_path_including_source_by_entity_id where the excluded entities is empty."""
    entity_id_1 = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1004")
    entity_id_2 = get_entity_id_from_record_id(sz_engine, "WATCHLIST", "1007")
    max_degree = 3
    excluded_entities = {}
    required_dsrcs = {"DATA_SOURCES": ["WATCHLIST"]}
    actual = sz_engine.find_path_including_source_by_entity_id(
        entity_id_1, entity_id_2, max_degree, excluded_entities, required_dsrcs
    )
    actual_dict = json.loads(actual)
    assert schema(path_schema) == actual_dict


def test_find_path_including_source_by_entity_id_required_dsrcs_empty(
    sz_engine,
) -> None:
    """Test find_path_including_source_by_entity_id where the required data sources is empty."""
    entity_id_1 = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1004")
    entity_id_2 = get_entity_id_from_record_id(sz_engine, "WATCHLIST", "1007")
    entity_id_3 = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1005")
    max_degree = 3
    excluded_entities = {"ENTITIES": [{"ENTITY_ID": entity_id_3}]}
    required_dsrcs = {}
    actual = sz_engine.find_path_including_source_by_entity_id(
        entity_id_1, entity_id_2, max_degree, excluded_entities, required_dsrcs
    )
    actual_dict = json.loads(actual)
    assert schema(path_schema) == actual_dict


def test_find_path_including_source_by_record_id_bad_data_source_code(
    sz_engine,
) -> None:
    """Test find_path_including_source_by_record_id with non-existent data source."""
    data_source_code_1 = "DOESN'T EXIST"
    record_id_1 = "1001"
    data_source_code_2 = "WATCHLIST"
    record_id_2 = "1007"
    max_degree = 3
    excluded_entities = {"ENTITIES": [{"ENTITY_ID": 6}]}
    required_dsrcs = {"DATA_SOURCES": ["WATCHLIST"]}
    with pytest.raises(SzError):
        sz_engine.find_path_including_source_by_record_id(
            data_source_code_1,
            record_id_1,
            data_source_code_2,
            record_id_2,
            max_degree,
            excluded_entities,
            required_dsrcs,
        )


def test_find_path_including_source_by_record_id_excluded_entities_empty(
    sz_engine,
) -> None:
    """Test find_path_including_source_by_record_id where the excluded entities is empty."""
    data_source_code_1 = "CUSTOMERS"
    record_id_1 = "1001"
    data_source_code_2 = "WATCHLIST"
    record_id_2 = "1007"
    max_degree = 3
    excluded_entities = {}
    required_dsrcs = '{"DATA_SOURCES": ["WATCHLIST"]}'
    actual = sz_engine.find_path_including_source_by_record_id(
        data_source_code_1,
        record_id_1,
        data_source_code_2,
        record_id_2,
        max_degree,
        excluded_entities,
        required_dsrcs,
    )
    actual_dict = json.loads(actual)
    assert schema(path_schema) == actual_dict


def test_find_path_including_source_by_record_id_required_dsrcs_empty(
    sz_engine,
) -> None:
    """Test find_path_including_source_by_record_id where the required data sources is empty."""
    data_source_code_1 = "CUSTOMERS"
    record_id_1 = "1001"
    data_source_code_2 = "WATCHLIST"
    record_id_2 = "1007"
    max_degree = 3
    excluded_entities = {"ENTITIES": [{"ENTITY_ID": 6}]}
    required_dsrcs = {}
    actual = sz_engine.find_path_including_source_by_record_id(
        data_source_code_1,
        record_id_1,
        data_source_code_2,
        record_id_2,
        max_degree,
        excluded_entities,
        required_dsrcs,
    )
    actual_dict = json.loads(actual)
    assert schema(path_schema) == actual_dict


def test_get_active_config_id(sz_engine: szengine.SzEngine) -> None:
    """Test get_active_config_id"""
    actual = sz_engine.get_active_config_id()
    assert actual >= 0


def test_get_entity_by_entity_id(
    sz_engine,
) -> None:
    """Test get_entity_by_entity_id."""
    entity_id = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001")
    actual = sz_engine.get_entity_by_entity_id(entity_id)
    actual_dict = json.loads(actual)
    assert schema(resolved_entity_schema) == actual_dict


def test_get_entity_by_entity_id_bad_entity_ids(sz_engine: szengine.SzEngine) -> None:
    """Test get_entity_by_entity_id with non-existent entities."""
    entity_id = 9999999999999999
    with pytest.raises(SzError):
        sz_engine.get_entity_by_entity_id(entity_id)


def test_get_entity_by_entity_id_return_dict_type(sz_engine: szengine.SzEngine) -> None:
    """Test find_get_entity_by_entity_id_return_dict returns a dict"""
    entity_id = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001")
    actual = sz_engine.get_entity_by_entity_id_return_dict(entity_id)
    assert isinstance(actual, dict)


def test_get_entity_by_record_id(sz_engine: szengine.SzEngine) -> None:
    """Test get_entity_by_record_id."""
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    actual = sz_engine.get_entity_by_record_id(data_source_code, record_id)
    actual_dict = json.loads(actual)
    assert schema(resolved_entity_schema) == actual_dict


def test_get_entity_by_record_id_bad_data_source_code(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test get_entity_by_record_id with non-existent data source."""
    data_source_code = "DOESN'T EXIST"
    record_id = "1001"
    with pytest.raises(SzError):
        sz_engine.get_entity_by_record_id(data_source_code, record_id)


def test_get_entity_by_record_id_bad_record_id(sz_engine: szengine.SzEngine) -> None:
    """Test get_entity_by_record_id with non-existent record id."""
    data_source_code = "CUSTOMERS"
    record_id = "9999999999999999"
    with pytest.raises(SzError):
        sz_engine.get_entity_by_record_id(data_source_code, record_id)


def test_get_record(sz_engine: szengine.SzEngine) -> None:
    """Test get_record."""
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    actual = sz_engine.get_record(data_source_code, record_id)
    actual_dict = json.loads(actual)
    assert schema(record_schema) == actual_dict


def test_get_record_bad_data_source_code(sz_engine: szengine.SzEngine) -> None:
    """Test get_record with non-existent data source."""
    data_source_code = "DOESN'T EXIST"
    record_id = "1001"
    with pytest.raises(SzError):
        sz_engine.get_record(data_source_code, record_id)


def test_get_record_bad_record_id(sz_engine: szengine.SzEngine) -> None:
    """Test get_record with non-existent record id."""
    data_source_code = "CUSTOMERS"
    record_id = "9999999999999999"
    with pytest.raises(SzError):
        sz_engine.get_record(data_source_code, record_id)


def test_get_record_return_dict_type(sz_engine: szengine.SzEngine) -> None:
    """Test get_record_return_dict returns a dict"""
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    actual = sz_engine.get_record_return_dict(data_source_code, record_id)
    assert isinstance(actual, dict)


def test_get_repository_last_modified_time(sz_engine: szengine.SzEngine) -> None:
    """Test get_repository_last_modified_time"""
    actual = sz_engine.get_repository_last_modified_time()
    assert actual >= 0


def test_get_virtual_entity_by_record_id_as_dict(
    sz_engine,
) -> None:
    """Test get_virtual_entity_by_record_id with record_list as a dict."""
    record_list = {
        "RECORDS": [
            {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1001"},
            {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1022"},
        ]
    }
    actual = sz_engine.get_virtual_entity_by_record_id(record_list)
    actual_dict = json.loads(actual)
    assert schema(virtual_entity_schema) == actual_dict


def test_get_virtual_entity_by_record_id_as_str(
    sz_engine,
) -> None:
    """Test get_virtual_entity_by_record_id with record_list as a string."""
    record_list = (
        '{"RECORDS": [{"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1001"},'
        ' {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1022"}]}'
    )
    actual = sz_engine.get_virtual_entity_by_record_id(record_list)
    actual_dict = json.loads(actual)
    assert schema(virtual_entity_schema) == actual_dict


def test_get_virtual_entity_by_record_id_bad_data_source_code(
    sz_engine,
) -> None:
    """Test get_virtual_entity_by_record_id with non-existent data source."""
    record_list = {
        "RECORDS": [
            {"DATA_SOURCE": "DOESN'T EXIST", "RECORD_ID": "1001"},
            {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1022"},
        ]
    }
    with pytest.raises(SzError):
        sz_engine.get_virtual_entity_by_record_id(record_list)


def test_get_virtual_entity_by_record_id_bad_record_id(
    sz_engine,
) -> None:
    """Test get_virtual_entity_by_record_id with non-existent record id."""
    record_list = {
        "RECORDS": [
            {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "9999999999999999"},
            {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1022"},
        ]
    }
    with pytest.raises(SzError):
        sz_engine.get_virtual_entity_by_record_id(record_list)


def test_get_virtual_entity_by_record_id_return_dict_type(
    sz_engine: szengine.SzEngine,
) -> None:
    """Test get_virtual_entity_by_record_id_return_dict returns a dict"""
    record_list = {
        "RECORDS": [
            {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1001"},
            {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1022"},
        ]
    }
    actual = sz_engine.get_virtual_entity_by_record_id_return_dict(record_list)
    assert isinstance(actual, dict)


def test_how_entity_by_entity_id(sz_engine: szengine.SzEngine) -> None:
    """Test how_entity_by_entity_id."""
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    entity_id = get_entity_id_from_record_id(sz_engine, data_source_code, record_id)
    actual = sz_engine.how_entity_by_entity_id(entity_id)
    actual_dict = json.loads(actual)
    assert schema(how_results_schema) == actual_dict


def test_how_entity_by_entity_id_bad_entity_id(sz_engine: szengine.SzEngine) -> None:
    """Test how_entity_by_entity_id with non-existent entity."""
    entity_id = "9999999999999999"
    with pytest.raises(SzError):
        sz_engine.how_entity_by_entity_id(entity_id)  # type: ignore[arg-type]


def test_how_entity_by_entity_id_return_dict_type(sz_engine: szengine.SzEngine) -> None:
    """Test how_entity_by_entity_id_return_dict returns a dict"""
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    entity_id = get_entity_id_from_record_id(sz_engine, data_source_code, record_id)
    actual = sz_engine.how_entity_by_entity_id_return_dict(entity_id)
    assert isinstance(actual, dict)


# TODO Add testing bad args
def test_init_and_destroy(engine_vars) -> None:
    """Test init and destroy."""
    module_name = "Test"
    ini_params = engine_vars["SETTINGS"]
    sz_engine_init_destroy = szengine.SzEngine()
    sz_engine_init_destroy.initialize(module_name, ini_params)
    sz_engine_init_destroy.destroy()


# TODO Add test for constructor to take init_config_id when modified g2engine.py
# def test_init_with_config_id(engine_vars) -> None:
#     """Test init_with_config_id."""
#     module_name = "Test"
#     ini_params = engine_vars["SETTINGS"]
#     sz_engine_2 = g2engine.G2Engine()
#     sz_engine_2.initialize(module_name, ini_params)
#     init_config_id = sz_engine_2.get_active_config_id()
#     sz_engine_2.destroy()
#     sz_engine_2 = g2engine.G2Engine()
#     sz_engine_2.init_with_config_id(module_name, ini_params, init_config_id)


# NOTE Having issues with this, coming back to...
# def test_init_with_config_id_bad_config_id(engine_vars) -> None:
#     """Test init_with_config_id with non-existent config id."""
#     module_name = "Test"
#     ini_params = engine_vars["SETTINGS"]
#     init_config_id = 0
#     sz_engine_with_id = g2engine.G2Engine()
#     with pytest.raises(g2exception.SzError):
#         sz_engine_with_id.init_with_config_id(module_name, ini_params, init_config_id)


def test_prime_engine(sz_engine: szengine.SzEngine) -> None:
    """Test prime_engine."""
    sz_engine.prime_engine()


# NOTE Don't need to test a non-existent entity, if not found it is ignored by the engine similar to delete_record
def test_reevaluate_entity(sz_engine: szengine.SzEngine) -> None:
    """Test reevaluate_entity."""
    entity_id = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001")
    sz_engine.reevaluate_entity(entity_id)


def test_reevaluate_record(sz_engine: szengine.SzEngine) -> None:
    """Test reevaluate_record."""
    data_source_code = "CUSTOMERS"
    record_id = "1001"
    sz_engine.reevaluate_record(data_source_code, record_id)


def test_reevaluate_record_bad_data_source_code(sz_engine: szengine.SzEngine) -> None:
    """Test reevaluate_record with non-existent data source code."""
    data_source_code = "DOESN'T EXIST"
    record_id = "1001"
    with pytest.raises(SzError):
        sz_engine.reevaluate_record(data_source_code, record_id)


def test_reevaluate_record_bad_record_id(sz_engine: szengine.SzEngine) -> None:
    """Test reevaluate_record with non-existent record id."""
    data_source_code = "CUSTOMERS"
    record_id = "9999999999999999"
    with pytest.raises(SzError):
        sz_engine.reevaluate_record(data_source_code, record_id)


def test_reinitialize(sz_engine: szengine.SzEngine) -> None:
    """Test reinit."""
    config_id = sz_engine.get_active_config_id()
    sz_engine.reinitialize(config_id)


def test_reinitialize_bad_config_id(sz_engine: szengine.SzEngine) -> None:
    """Test reinit with bad config id."""
    active_config_id = sz_engine.get_active_config_id()
    config_id = 0
    try:
        with pytest.raises(SzError):
            sz_engine.reinitialize(config_id)
    finally:
        sz_engine.reinitialize(active_config_id)


def test_search_by_attributes(sz_engine: szengine.SzEngine) -> None:
    """Test search_by_attributes."""
    json_data = {"NAME_FULL": "robert smith", "DATE_OF_BIRTH": "12/11/1978"}
    actual = sz_engine.search_by_attributes(json_data)
    actual_dict = json.loads(actual)
    assert schema(search_schema) == actual_dict


def test_search_by_attributes_bad_json_data(sz_engine: szengine.SzEngine) -> None:
    """Test search_by_attributes with bad JSON string."""
    json_data = '{"NAME_FULL" "robert smith", "DATE_OF_BIRTH": "12/11/1978"}'
    with pytest.raises(SzError):
        sz_engine.search_by_attributes(json_data)


def test_search_by_attributes_return_dict_type(sz_engine: szengine.SzEngine) -> None:
    """Test search_by_attributes_return_dict returns a dict"""
    json_data = {"NAME_FULL": "robert smith", "DATE_OF_BIRTH": "12/11/1978"}
    actual = sz_engine.search_by_attributes_return_dict(json_data)
    assert isinstance(actual, dict)


# NOTE Having issues with this, coming back to...
# def test_stats(engine_vars) -> None:
#     """Test stats."""
#     # Use a fresh engine so stats are mostly blank to align to stats_schema
#     sz_engine_stats = g2engine.G2Engine(
#         engine_vars["INSTANCE_NAME"], engine_vars["SETTINGS"]
#     )
#     actual = sz_engine_stats.stats()
#     actual_dict = json.loads(actual)
#     assert schema(stats_schema) == actual_dict


# NOTE Following are going away in V4
# why_entity_by_entity_id
# why_entity_by_record_id


def test_why_entities(sz_engine: szengine.SzEngine) -> None:
    """Test why_entities."""
    entity_id_1 = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001")
    entity_id_2 = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1002")
    actual = sz_engine.why_entities(entity_id_1, entity_id_2)
    actual_dict = json.loads(actual)
    assert schema(why_entities_results_schema) == actual_dict


def test_why_entities_bad_entity_id(sz_engine: szengine.SzEngine) -> None:
    """Test why_entities with non-existent entity."""
    entity_id_1 = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001")
    entity_id_2 = 9999999999999999
    with pytest.raises(SzError):
        sz_engine.why_entities(entity_id_1, entity_id_2)


def test_why_entities_return_dict_type(sz_engine: szengine.SzEngine) -> None:
    """Test why_entities_return_dict returns a dict"""
    entity_id_1 = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1001")
    entity_id_2 = get_entity_id_from_record_id(sz_engine, "CUSTOMERS", "1002")
    actual = sz_engine.why_entities_return_dict(entity_id_1, entity_id_2)
    assert isinstance(actual, dict)


def test_why_records(sz_engine: szengine.SzEngine) -> None:
    """Test why_records."""
    data_source_code_1 = "CUSTOMERS"
    record_id_1 = "1001"
    data_source_code_2 = "CUSTOMERS"
    record_id_2 = "1002"
    actual = sz_engine.why_records(
        data_source_code_1, record_id_1, data_source_code_2, record_id_2
    )
    actual_dict = json.loads(actual)
    assert schema(why_entity_results_schema) == actual_dict


def test_why_records_bad_data_source_code(sz_engine: szengine.SzEngine) -> None:
    """Test why_records with non-existent data source."""
    data_source_code_1 = "DOESN'T EXIST"
    record_id_1 = "1001"
    data_source_code_2 = "CUSTOMERS"
    record_id_2 = "1002"
    with pytest.raises(SzError):
        sz_engine.why_records(
            data_source_code_1, record_id_1, data_source_code_2, record_id_2
        )


def test_why_records_bad_record_id(sz_engine: szengine.SzEngine) -> None:
    """Test why_records with non-existent record id."""
    data_source_code_1 = "CUSTOMERS"
    record_id_1 = "9999999999999999"
    data_source_code_2 = "CUSTOMERS"
    record_id_2 = "1002"
    with pytest.raises(SzError):
        sz_engine.why_records(
            data_source_code_1, record_id_1, data_source_code_2, record_id_2
        )


def test_why_records_return_dict_type(sz_engine: szengine.SzEngine) -> None:
    """Test why_records_return_dict returns a dict"""
    data_source_code_1 = "CUSTOMERS"
    record_id_1 = "1001"
    data_source_code_2 = "CUSTOMERS"
    record_id_2 = "1002"
    actual = sz_engine.why_records_return_dict(
        data_source_code_1, record_id_1, data_source_code_2, record_id_2
    )
    assert isinstance(actual, dict)


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# SzEngine fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="sz_config", scope="module")  # type: ignore[misc]
def szconfig_fixture(engine_vars) -> szconfig.SzConfig:
    """
    Single config object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    return szconfig.SzConfig(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )


@pytest.fixture(name="sz_configmanager", scope="module")  # type: ignore[misc]
def szconfigmanager_fixture(engine_vars) -> szconfigmanager.SzConfigManager:
    """
    Single configmanager object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    return szconfigmanager.SzConfigManager(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )


@pytest.fixture(name="sz_engine", scope="module")  # type: ignore[misc]
def szengine_fixture(engine_vars) -> szengine.SzEngine:
    """
    Single engine object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    return szengine.SzEngine(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------


def add_records(
    sz_engine: szengine.SzEngine, record_id_list: List[Tuple[str, str]]
) -> None:
    """Add all of the records in the list."""
    flags = SzEngineFlags.SZ_WITHOUT_INFO
    for record_identification in record_id_list:
        datasource = record_identification[0]
        record_id = record_identification[1]
        record = DATA_SOURCES.get(datasource, {}).get(record_id, {})
        sz_engine.add_record(
            record.get("DataSource", ""),
            record.get("Id", ""),
            record.get("Json", ""),
            flags,
        )


def add_records_truthset(sz_engine: szengine.SzEngine, do_redo=True) -> None:
    """Add all truth-set the records."""
    flags = SzEngineFlags.SZ_WITHOUT_INFO
    for record_set in DATA_SOURCES.values():
        for record in record_set.values():
            sz_engine.add_record(
                record.get("DataSource"),
                record.get("Id"),
                record.get("Json"),
                flags,
            )
    if do_redo:
        while sz_engine.count_redo_records() > 0:
            redo_record = sz_engine.get_redo_record()
            sz_engine.process_redo_record(redo_record, flags)


def delete_records(
    sz_engine: szengine.SzEngine, record_id_list: List[Tuple[str, str]]
) -> None:
    """Delete all of the records in the list."""
    flags = SzEngineFlags.SZ_WITHOUT_INFO
    for record_identification in record_id_list:
        datasource = record_identification[0]
        record_id = record_identification[1]
        record = DATA_SOURCES.get(datasource, {}).get(record_id, {})
        sz_engine.delete_record(
            record.get("DataSource", ""), record.get("Id", ""), flags
        )


def delete_records_truthset(sz_engine: szengine.SzEngine) -> None:
    """Delete all truth-set the records."""
    flags = SzEngineFlags.SZ_WITHOUT_INFO
    for record_set in DATA_SOURCES.values():
        for record in record_set.values():
            sz_engine.delete_record(record.get("DataSource"), record.get("Id"), flags)


def get_entity_id_from_record_id(
    sz_engine: szengine.SzEngine, data_source_code: str, record_id: str
) -> int:
    """Given a (datasource, record_id), return the entity ID."""
    entity_json = sz_engine.get_entity_by_record_id(data_source_code, record_id)
    entity = json.loads(entity_json)
    return int(entity.get("RESOLVED_ENTITY", {}).get("ENTITY_ID", 0))


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

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
# SzEngine schemas
# -----------------------------------------------------------------------------

add_record_with_info_schema = {
    "DATA_SOURCE": str,
    "RECORD_ID": str,
    "AFFECTED_ENTITIES": [{"ENTITY_ID": int}],
    "INTERESTING_ENTITIES": {"ENTITIES": []},
}

export_json_entity_report_schema = {
    "RESOLVED_ENTITY": {
        "ENTITY_ID": int,
        "ENTITY_NAME": str,
        "FEATURES": {},
        "RECORDS": [
            {
                "DATA_SOURCE": str,
                "RECORD_ID": str,
                "ENTITY_TYPE": str,
                "INTERNAL_ID": int,
                "ENTITY_KEY": str,
                "ENTITY_DESC": str,
                "MATCH_KEY": str,
                "MATCH_LEVEL": int,
                "MATCH_LEVEL_CODE": str,
                "ERRULE_CODE": str,
                "LAST_SEEN_DT": str,
            }
        ],
    },
    "RELATED_ENTITIES": [{}],
}


g2_config_schema = {
    "G2_CONFIG": {
        "CFG_ETYPE": [
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
                "FELEM_ID": int,
                "EXEC_ORDER": int,
                "DISPLAY_LEVEL": int,
                "DISPLAY_DELIM": Or(str, None),
                "DERIVED": str,
            },
        ],
        "CFG_FELEM": [
            {
                "FELEM_ID": int,
                "FELEM_CODE": str,
                "TOKENIZE": str,
                "DATA_TYPE": str,
            },
        ],
        "CFG_DSRC": [
            {
                "DSRC_ID": int,
                "DSRC_CODE": str,
                "DSRC_DESC": str,
                "DSRC_RELY": int,
                "RETENTION_LEVEL": str,
                "CONVERSATIONAL": str,
            },
        ],
        "CFG_EFBOM": [
            {
                "EFCALL_ID": int,
                "FTYPE_ID": int,
                "FELEM_ID": int,
                "EXEC_ORDER": int,
                "FELEM_REQ": str,
            },
        ],
        "CFG_EFUNC": [
            {
                "EFUNC_ID": int,
                "EFUNC_CODE": str,
                "FUNC_LIB": str,
                "FUNC_VER": str,
                "CONNECT_STR": str,
                "LANGUAGE": Or(str, None),
                "JAVA_CLASS_NAME": Or(str, None),
            },
        ],
        "CFG_EFCALL": [
            {
                "EFCALL_ID": int,
                "FTYPE_ID": int,
                "FELEM_ID": int,
                "EFUNC_ID": int,
                "EXEC_ORDER": int,
                "EFEAT_FTYPE_ID": int,
                "IS_VIRTUAL": str,
            },
        ],
        "CFG_SFCALL": [
            {
                "SFCALL_ID": int,
                "FTYPE_ID": int,
                "FELEM_ID": int,
                "SFUNC_ID": int,
                "EXEC_ORDER": int,
            },
        ],
        "CFG_SFUNC": [
            {
                "SFUNC_ID": int,
                "SFUNC_CODE": str,
                "FUNC_LIB": str,
                "FUNC_VER": str,
                "CONNECT_STR": str,
                "LANGUAGE": Or(str, None),
                "JAVA_CLASS_NAME": Or(str, None),
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
                "FUNC_LIB": str,
                "FUNC_VER": str,
                "CONNECT_STR": str,
                "ANON_SUPPORT": str,
                "LANGUAGE": Or(str, None),
                "JAVA_CLASS_NAME": Or(str, None),
            },
        ],
        "CFG_CFCALL": [
            {
                "CFCALL_ID": int,
                "FTYPE_ID": int,
                "CFUNC_ID": int,
                "EXEC_ORDER": int,
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
                "ERRULE_DESC": str,
                "RESOLVE": str,
                "RELATE": str,
                "REF_SCORE": int,
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
                "FELEM_ID": int,
                "EXEC_ORDER": int,
            },
        ],
        "CFG_DFUNC": [
            {
                "DFUNC_ID": int,
                "DFUNC_CODE": str,
                "FUNC_LIB": str,
                "FUNC_VER": str,
                "CONNECT_STR": str,
                "ANON_SUPPORT": str,
                "LANGUAGE": Or(str, None),
                "JAVA_CLASS_NAME": Or(str, None),
            },
        ],
        "CFG_DFCALL": [
            {
                "DFCALL_ID": int,
                "FTYPE_ID": int,
                "DFUNC_ID": int,
                "EXEC_ORDER": int,
            },
        ],
        "CFG_DFBOM": [
            {
                "DFCALL_ID": int,
                "FTYPE_ID": int,
                "FELEM_ID": int,
                "EXEC_ORDER": int,
            },
        ],
        "CFG_CFRTN": [
            {
                "CFRTN_ID": int,
                "CFUNC_ID": int,
                "FTYPE_ID": int,
                "CFUNC_RTNVAL": str,
                "EXEC_ORDER": int,
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
                "REL_STRENGTH": int,
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
                "ADVANCED": str,
                "INTERNAL": str,
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
                            "RECORDS": [{"DATA_SOURCE": str, "RECORD_ID": str}],
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
    "ENTITY_PATHS": [{"START_ENTITY_ID": int, "END_ENTITY_ID": int, "ENTITIES": []}],
    "ENTITIES": [
        {
            "RESOLVED_ENTITY": {
                "ENTITY_ID": int,
                "ENTITY_NAME": str,
                "RECORD_SUMMARY": [
                    {
                        "DATA_SOURCE": str,
                        "RECORD_COUNT": int,
                        "FIRST_SEEN_DT": str,
                        "LAST_SEEN_DT": str,
                    }
                ],
                "LAST_SEEN_DT": str,
            },
            "RELATED_ENTITIES": [
                {
                    "ENTITY_ID": int,
                    "MATCH_LEVEL": int,
                    "MATCH_LEVEL_CODE": str,
                    "MATCH_KEY": str,
                    "ERRULE_CODE": str,
                    "IS_DISCLOSED": int,
                    "IS_AMBIGUOUS": int,
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
                "ENTITY_NAME": str,
                "RECORD_SUMMARY": [
                    {
                        "DATA_SOURCE": str,
                        "RECORD_COUNT": int,
                        "FIRST_SEEN_DT": str,
                        "LAST_SEEN_DT": str,
                    }
                ],
                "LAST_SEEN_DT": str,
            },
            "RELATED_ENTITIES": [
                {
                    "ENTITY_ID": int,
                    "MATCH_LEVEL": int,
                    "MATCH_LEVEL_CODE": str,
                    "MATCH_KEY": str,
                    "ERRULE_CODE": str,
                    "IS_DISCLOSED": int,
                    "IS_AMBIGUOUS": int,
                }
            ],
        }
    ],
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
    "ENTITY_TYPE": str,
    "DSRC_ACTION": str,
}

resolved_entity_schema = {
    "RESOLVED_ENTITY": {
        "ENTITY_ID": int,
        "ENTITY_NAME": str,
        "FEATURES": {},
        "RECORD_SUMMARY": [
            {
                "DATA_SOURCE": str,
                "RECORD_COUNT": int,
                "FIRST_SEEN_DT": str,
                "LAST_SEEN_DT": str,
            }
        ],
        "LAST_SEEN_DT": str,
        "RECORDS": [
            {
                "DATA_SOURCE": str,
                "RECORD_ID": str,
                "ENTITY_TYPE": str,
                "INTERNAL_ID": int,
                "ENTITY_KEY": str,
                "ENTITY_DESC": str,
                "MATCH_KEY": str,
                "MATCH_LEVEL": int,
                "MATCH_LEVEL_CODE": str,
                "ERRULE_CODE": str,
                "LAST_SEEN_DT": str,
            },
        ],
    },
    "RELATED_ENTITIES": [{}],
}

search_schema = {
    "RESOLVED_ENTITIES": [
        {
            "MATCH_INFO": {
                "MATCH_LEVEL": int,
                "MATCH_LEVEL_CODE": str,
                "MATCH_KEY": str,
                "ERRULE_CODE": str,
                "FEATURE_SCORES": {},
            },
            "ENTITY": {
                "RESOLVED_ENTITY": {
                    "ENTITY_ID": int,
                    "ENTITY_NAME": str,
                    "FEATURES": {},
                    "RECORD_SUMMARY": [
                        {
                            "DATA_SOURCE": str,
                            "RECORD_COUNT": int,
                            "FIRST_SEEN_DT": str,
                            "LAST_SEEN_DT": str,
                        }
                    ],
                    "LAST_SEEN_DT": str,
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
        "unresolveTest": int,
        "abortedUnresolve": int,
        "gnrScorersUsed": int,
        "unresolveTriggers": {},
        "reresolveTriggers": {
            "abortRetry": int,
            "unresolveMovement": int,
            "multipleResolvableCandidates": int,
            "resolveNewFeatures": int,
            "newFeatureFTypes": [],
        },
        "reresolveSkipped": int,
        "filteredObsFeat": int,
        "expressedFeatureCalls": [],
        "expressedFeaturesCreated": [],
        "scoredPairs": [],
        "cacheHit": [],
        "cacheMiss": [],
        "redoTriggers": [],
        "latchContention": [],
        "highContentionFeat": [],
        "highContentionResEnt": [],
        "genericDetect": [],
        "candidateBuilders": [],
        "suppressedCandidateBuilders": [],
        "suppressedScoredFeatureType": [],
        "reducedScoredFeatureType": [],
        "suppressedDisclosedRelationshipDomainCount": int,
        "CorruptEntityTestDiagnosis": {},
        "threadState": {},
        "systemResources": {"initResources": [{}], "currResources": [{}]},
    }
}

virtual_entity_schema = {
    "RESOLVED_ENTITY": {
        "ENTITY_ID": int,
        "ENTITY_NAME": str,
        "FEATURES": {},
        "RECORD_SUMMARY": [
            {
                "DATA_SOURCE": str,
                "RECORD_COUNT": int,
                "FIRST_SEEN_DT": str,
                "LAST_SEEN_DT": str,
            }
        ],
        "LAST_SEEN_DT": str,
        "RECORDS": [
            {
                "DATA_SOURCE": str,
                "RECORD_ID": str,
                "ENTITY_TYPE": str,
                "INTERNAL_ID": int,
                "ENTITY_KEY": str,
                "ENTITY_DESC": str,
                "LAST_SEEN_DT": str,
                "FEATURES": [{"LIB_FEAT_ID": int}],
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
                "ENTITY_NAME": str,
                "FEATURES": {},
                "RECORD_SUMMARY": [{}],
                "LAST_SEEN_DT": str,
                "RECORDS": [
                    {
                        "DATA_SOURCE": str,
                        "RECORD_ID": str,
                        "ENTITY_TYPE": str,
                        "INTERNAL_ID": int,
                        "ENTITY_KEY": str,
                        "ENTITY_DESC": str,
                        "MATCH_KEY": str,
                        "MATCH_LEVEL": int,
                        "MATCH_LEVEL_CODE": str,
                        "ERRULE_CODE": str,
                        "LAST_SEEN_DT": str,
                        "FEATURES": [{}],
                    }
                ],
            },
            "RELATED_ENTITIES": [{}],
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
                "ENTITY_NAME": str,
                "FEATURES": {},
                "RECORD_SUMMARY": [{}],
                "LAST_SEEN_DT": str,
                "RECORDS": [
                    {
                        "DATA_SOURCE": str,
                        "RECORD_ID": str,
                        "ENTITY_TYPE": str,
                        "INTERNAL_ID": int,
                        "ENTITY_KEY": str,
                        "ENTITY_DESC": str,
                        "MATCH_KEY": str,
                        "MATCH_LEVEL": int,
                        "MATCH_LEVEL_CODE": str,
                        "ERRULE_CODE": str,
                        "LAST_SEEN_DT": str,
                        "FEATURES": [{}],
                    }
                ],
            },
            "RELATED_ENTITIES": [{}],
        }
    ],
}
