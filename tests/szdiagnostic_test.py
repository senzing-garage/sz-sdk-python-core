import json
from ctypes import ArgumentError
from typing import Any, Dict

import pytest
from pytest_schema import schema

from senzing import SZ_NO_LOGGING, SzConfigManager, SzDiagnostic, SzEngine, SzError

# -----------------------------------------------------------------------------
# SzDiagnostic testcases
# -----------------------------------------------------------------------------


def test_exception(sz_diagnostic: SzDiagnostic) -> None:
    """Test exceptions."""
    with pytest.raises(Exception):
        sz_diagnostic.check_result(-1)


def test_constructor(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    actual = SzDiagnostic()
    actual._initialize(  # pylint: disable=W0212
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    assert isinstance(actual, SzDiagnostic)


def test_constructor_dict(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    actual = SzDiagnostic()
    actual._initialize(  # pylint: disable=W0212
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS_DICT"],
    )
    assert isinstance(actual, SzDiagnostic)


# def test_constructor_bad_instance_name(engine_vars: Dict[Any, Any]) -> None:
#     """Test constructor."""
#     bad_instance_name = ""
#     with pytest.raises(SzError):
#         actual = SzDiagnostic()
#         actual._initialize(  # pylint: disable=W0212
#             bad_instance_name,
#             engine_vars["SETTINGS"],
#         )
#         assert isinstance(actual, SzDiagnostic)


def test_constructor_bad_settings(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    bad_settings = ""
    with pytest.raises(SzError):
        actual = SzDiagnostic()
        actual._initialize(  # pylint: disable=W0212
            engine_vars["INSTANCE_NAME"],
            bad_settings,
        )
        assert isinstance(actual, SzDiagnostic)


def test_check_datastore_performance(sz_diagnostic: SzDiagnostic) -> None:
    """Test SzDiagnostic().check_datastore_performance()."""
    seconds_to_run = 3
    actual = sz_diagnostic.check_datastore_performance(seconds_to_run)
    actual_as_dict = json.loads(actual)
    assert schema(check_datastore_performance_schema) == actual_as_dict


def test_check_datastore_performance_bad_seconds_to_run_type(
    sz_diagnostic: SzDiagnostic,
) -> None:
    """Test SzDiagnostic().check_datastore_performance()."""
    bad_seconds_to_run = "string"
    with pytest.raises(TypeError):
        sz_diagnostic.check_datastore_performance(bad_seconds_to_run)  # type: ignore[arg-type]


def test_check_datastore_performance_bad_seconds_to_run_value(
    sz_diagnostic: SzDiagnostic,
) -> None:
    """Test SzDiagnostic().check_datastore_performance()."""
    bad_seconds_to_run = -1
    sz_diagnostic.check_datastore_performance(bad_seconds_to_run)
    actual = sz_diagnostic.check_datastore_performance(bad_seconds_to_run)
    actual_as_dict = json.loads(actual)
    assert schema(check_datastore_performance_schema) == actual_as_dict

def test_double_destroy(engine_vars: Dict[Any, Any]) -> None:
    """Test calling destroy twice."""
    actual = SzDiagnostic()
    actual._initialize(  # pylint: disable=W0212
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS_DICT"],
    )
    actual._destroy()  # pylint: disable=W0212
    actual._destroy()  # pylint: disable=W0212


def test_get_datastore_info(sz_diagnostic: SzDiagnostic) -> None:
    """Test SzDiagnostic().get_datastore_info()."""
    actual = sz_diagnostic.get_datastore_info()
    actual_as_dict = json.loads(actual)
    assert schema(get_datastore_info_schema) == actual_as_dict


def test_get_feature(sz_diagnostic: SzDiagnostic, sz_engine: SzEngine) -> None:
    """# TODO"""
    data_source_code = "TEST"
    record_id = "1"
    record_definition: str = '{"NAME_FULL": "Joe Blogs", "DATE_OF_BIRTH": "07/07/1976"}'
    sz_engine.add_record(data_source_code, record_id, record_definition)
    actual = sz_diagnostic.get_feature(1)
    actual_as_dict = json.loads(actual)
    assert schema(get_feature_schema) == actual_as_dict


def test_get_feature_unknown_id(sz_diagnostic: SzDiagnostic) -> None:
    """# TODO"""
    with pytest.raises(SzError):
        _ = sz_diagnostic.get_feature(111111111111111111)


def test_reinitialize(
    sz_diagnostic: SzDiagnostic, sz_configmanager: SzConfigManager
) -> None:
    """Test SzDiagnostic().reinit() with current config ID."""
    default_config_id = sz_configmanager.get_default_config_id()
    try:
        sz_diagnostic.reinitialize(default_config_id)
    except SzError:
        assert False


def test_reinitialize_bad_config_id(sz_diagnostic: SzDiagnostic) -> None:
    """Test SzDiagnostic().reinit() with current config ID."""
    bad_default_config_id = "string"
    with pytest.raises(ArgumentError):
        sz_diagnostic.reinitialize(bad_default_config_id)  # type: ignore[arg-type]


def test_reinitialize_missing_config_id(sz_diagnostic: SzDiagnostic) -> None:
    """Test SzDiagnostic().reinit() raising error."""
    with pytest.raises(SzError):
        sz_diagnostic.reinitialize(999)


# def test_initialize_and_destroy(
#     sz_diagnostic: SzDiagnostic, engine_vars: Dict[Any, Any]
# ) -> None:
#     """Test SzDiagnostic().init() and SzDiagnostic.destroy()."""
#     instance_name = engine_vars["INSTANCE_NAME"]
#     settings = engine_vars["SETTINGS"]
#     verbose_logging = SzEngineFlags.SZ_NO_LOGGING
#     sz_diagnostic.initialize(instance_name, settings, verbose_logging)
#     sz_diagnostic.destroy()


# TODO: Uncomment testcase after Senzing code build 2024_05_01__07_22.
# def test_init_and_destroy_again(sz_diagnostic, engine_vars):
#     """Test SzDiagnostic().init() and SzDiagnostic.destroy()."""
#     sz_diagnostic.initialize(engine_vars["INSTANCE_NAME"], engine_vars["SETTINGS"], 0)
#     sz_diagnostic.destroy()


# TODO: Uncomment testcase after Senzing code build 2024_05_01__07_22.
# def test_initialize_with_config_id_and_destroy(sz_configmanager, engine_vars):
#     """Test SzDiagnostic().init_with_config_id() and SzDiagnostic.destroy()."""
#     # TODO: This has the same issue as test_init_and_destroy_2
#     default_config_id = sz_configmanager.get_default_config_id()
#     sz_diagnostic = SzDiagnostic()
#     sz_diagnostic.initialize(
#         instance_name=engine_vars["INSTANCE_NAME"],
#         settings=engine_vars["SETTINGS"],
#         config_id=default_config_id,
#         verbose_logging=0,
#     )
#     sz_diagnostic.destroy()


# TODO: Uncomment testcase after Senzing code build 2024_05_01__07_22.
# def test_context_managment(engine_vars: Dict[Any, Any]) -> None:
#     """Test the use of SzDiagnostic in context."""
#     with SzDiagnostic(
#         instance_name=engine_vars["INSTANCE_NAME"],
#         settings=engine_vars["SETTINGS"],
#         verbose_logging=1,
#     ) as sz_diagnostic:
#         actual = sz_diagnostic.get_datastore_info()
#         actual_json = json.loads(actual)
#         assert schema(get_datastore_info_schema) == actual_json


# -----------------------------------------------------------------------------
# SzDiagnostic fixtures
# -----------------------------------------------------------------------------


# @pytest.fixture(name="sz_configmanager", scope="module")
@pytest.fixture(name="sz_configmanager", scope="function")
def szconfigmanager_fixture(engine_vars: Dict[Any, Any]) -> SzConfigManager:
    """Single szconfigmanager object to use for all tests.
    engine_vars is returned from conftest.pys"""
    result = SzConfigManager()
    result._initialize(
        instance_name=engine_vars["INSTANCE_NAME"],
        settings=engine_vars["SETTINGS"],
        verbose_logging=0,
    )
    return result


# @pytest.fixture(name="sz_diagnostic", scope="module")
@pytest.fixture(name="sz_diagnostic", scope="function")
def szdiagnostic_fixture(engine_vars: Dict[Any, Any]) -> SzDiagnostic:
    """Single szdiagnostic object to use for all tests.
    engine_vars is returned from conftest.pys"""
    result = SzDiagnostic()
    result._initialize(
        instance_name=engine_vars["INSTANCE_NAME"],
        settings=engine_vars["SETTINGS"],
        config_id=0,
        verbose_logging=0,
    )
    return result


@pytest.fixture(name="sz_engine", scope="function")
def szengine_fixture(engine_vars: Dict[Any, Any]) -> SzEngine:
    """Single szengine object to use for all tests.
    engine_vars is returned from conftest.pys"""
    result = SzEngine()
    result._initialize(
        instance_name=engine_vars["INSTANCE_NAME"],
        settings=engine_vars["SETTINGS"],
        config_id=0,
        verbose_logging=0,
    )
    return result


# -----------------------------------------------------------------------------
# SzDiagnostic schemas
# -----------------------------------------------------------------------------


get_datastore_info_schema = {
    "dataStores": [
        {
            "id": str,
            "type": str,
            "location": str,
        }
    ],
}

check_datastore_performance_schema = {"numRecordsInserted": int, "insertTime": int}

get_feature_schema = {"LIB_FEAT_ID": int, "FTYPE_CODE": str, "ELEMENTS": [{str: str}]}
# '{"LIB_FEAT_ID":1,"FTYPE_CODE":"NAME","ELEMENTS":[{"FELEM_CODE":"TOKENIZED_NM","FELEM_VALUE":"ROBERT|SMITH"},{"FELEM_CODE":"CATEGORY","FELEM_VALUE":"PERSON"},{"FELEM_CODE":"CULTURE","FELEM_VALUE":"ANGLO"},{"FELEM_CODE":"GIVEN_NAME","FELEM_VALUE":"Robert"},{"FELEM_CODE":"SUR_NAME","FELEM_VALUE":"Smith"},{"FELEM_CODE":"FULL_NAME","FELEM_VALUE":"Robert Smith"}]}'
