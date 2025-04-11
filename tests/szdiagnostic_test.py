import json
from typing import Any, Dict

import pytest
from pytest_schema import schema
from senzing import SzConfigManager, SzDiagnostic, SzEngine, SzError

from senzing_core import SzConfigManagerCore, SzDiagnosticCore, SzEngineCore

# -----------------------------------------------------------------------------
# Testcases
# -----------------------------------------------------------------------------


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
    # with pytest.raises(SzDatabaseError):
    #     sz_diagnostic.check_datastore_performance(bad_seconds_to_run)
    actual = sz_diagnostic.check_datastore_performance(bad_seconds_to_run)
    actual_as_dict = json.loads(actual)
    assert schema(check_datastore_performance_schema) == actual_as_dict


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


# -----------------------------------------------------------------------------
# Unique testcases
# -----------------------------------------------------------------------------


def test_constructor(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    actual = SzDiagnosticCore()
    actual.initialize(  # pylint: disable=W0212
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    assert isinstance(actual, SzDiagnostic)


def test_constructor_dict(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    actual = SzDiagnosticCore()
    actual.initialize(  # pylint: disable=W0212
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS_DICT"],
    )
    assert isinstance(actual, SzDiagnostic)


def test_destroy(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    actual = SzDiagnosticCore()
    actual.initialize(  # pylint: disable=W0212
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    actual._destroy()  # pylint: disable=W0212


def test_exception(sz_configmanager: SzConfigManagerCore) -> None:
    """Test exceptions."""
    with pytest.raises(Exception):
        sz_configmanager.check_result(-1)


def test_reinitialize(sz_diagnostic: SzDiagnosticCore, sz_configmanager: SzConfigManagerCore) -> None:
    """Test SzDiagnosticCore().reinit() with current config ID."""
    default_config_id = sz_configmanager.get_default_config_id()
    try:
        sz_diagnostic._reinitialize(default_config_id)  # pylint: disable=W0212
    except SzError:
        assert False


def test_reinitialize_bad_config_id(sz_diagnostic: SzDiagnosticCore) -> None:
    """Test SzDiagnosticCore().reinit() with current config ID."""
    bad_default_config_id = "string"
    # pylint: disable=W0212
    with pytest.raises(TypeError):
        sz_diagnostic._reinitialize(bad_default_config_id)  # type: ignore[arg-type]


def test_reinitialize_missing_config_id(sz_diagnostic: SzDiagnosticCore) -> None:
    """Test SzDiagnosticCore().reinit() raising error."""
    with pytest.raises(SzError):
        sz_diagnostic._reinitialize(999)  # pylint: disable=W0212


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="sz_configmanager", scope="function")
def szconfigmanager_fixture(engine_vars: Dict[Any, Any]) -> SzConfigManager:
    """Single szconfigmanager object to use for all tests.
    engine_vars is returned from conftest.pys"""
    result = SzConfigManagerCore()
    result.initialize(  # pylint: disable=W0212
        instance_name=engine_vars["INSTANCE_NAME"],
        settings=engine_vars["SETTINGS"],
        verbose_logging=0,
    )
    return result


@pytest.fixture(name="sz_diagnostic", scope="function")
def szdiagnostic_fixture(engine_vars: Dict[Any, Any]) -> SzDiagnostic:
    """Single szdiagnostic object to use for all tests.
    engine_vars is returned from conftest.pys"""
    result = SzDiagnosticCore()
    result.initialize(  # pylint: disable=W0212
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
    result = SzEngineCore()
    result.initialize(  # pylint: disable=W0212
        instance_name=engine_vars["INSTANCE_NAME"],
        settings=engine_vars["SETTINGS"],
        config_id=0,
        verbose_logging=0,
    )
    return result


# -----------------------------------------------------------------------------
# Schemas
# -----------------------------------------------------------------------------

check_datastore_performance_schema = {"numRecordsInserted": int, "insertTime": int}

get_datastore_info_schema = {
    "dataStores": [
        {
            "id": str,
            "type": str,
            "location": str,
        }
    ],
}

get_feature_schema = {"LIB_FEAT_ID": int, "FTYPE_CODE": str, "ELEMENTS": [{str: str}]}
