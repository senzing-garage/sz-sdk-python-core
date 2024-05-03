from ctypes import ArgumentError
from typing import Any, Dict

import pytest
from pytest_schema import schema
from senzing_dict import SzConfigManager as SzConfigManagerDict
from senzing_dict import SzDiagnostic as SzDiagnosticDict

from senzing import SzConfigManager, SzDiagnostic, SzError

# -----------------------------------------------------------------------------
# SzDiagnostic testcases
# -----------------------------------------------------------------------------


def test_constructor(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    sz_diagnostic = SzDiagnostic(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    actual = SzDiagnosticDict(sz_diagnostic)
    assert isinstance(actual, SzDiagnosticDict)


def test_check_datastore_performance(sz_diagnostic: SzDiagnostic) -> None:
    """Test SzDiagnostic().check_datastore_performance()."""
    seconds_to_run = 3
    actual = sz_diagnostic.check_datastore_performance(seconds_to_run)
    assert schema(check_datastore_performance_schema) == actual


def test_check_datastore_performance_bad_seconds_to_run_type(
    sz_diagnostic: SzDiagnostic,
) -> None:
    """Test SzDiagnostic().check_datastore_performance()."""
    bad_seconds_to_run = "string"
    with pytest.raises(ArgumentError):
        sz_diagnostic.check_datastore_performance(bad_seconds_to_run)  # type: ignore[arg-type]


def test_check_datastore_performance_bad_seconds_to_run_value(
    sz_diagnostic: SzDiagnostic,
) -> None:
    """Test SzDiagnostic().check_datastore_performance()."""
    bad_seconds_to_run = -1
    sz_diagnostic.check_datastore_performance(bad_seconds_to_run)


def test_get_datastore_info(sz_diagnostic: SzDiagnostic) -> None:
    """Test SzDiagnostic().get_datastore_info()."""
    actual = sz_diagnostic.get_datastore_info()
    assert schema(get_datastore_info_schema) == actual


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


def test_reinitialize_missing_config_id(
    sz_diagnostic: SzDiagnostic,
) -> None:
    """Test SzDiagnostic().reinit() raising error."""
    with pytest.raises(SzError):
        sz_diagnostic.reinitialize(999)


def test_initialize_and_destroy(
    sz_diagnostic: SzDiagnostic, engine_vars: Dict[Any, Any]
) -> None:
    """Test SzDiagnostic().init() and SzDiagnostic.destroy()."""
    sz_diagnostic.initialize(engine_vars["INSTANCE_NAME"], engine_vars["SETTINGS"], 0)
    sz_diagnostic.destroy()


# -----------------------------------------------------------------------------
# SzDiagnostic fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="sz_configmanager", scope="module")
def szconfigmanager_instance_fixture(
    engine_vars: Dict[Any, Any]
) -> SzConfigManagerDict:
    """Single szconfigmanager object to use for all tests.
    build_engine_vars is returned from conftest.pys"""

    sz_configmanager = SzConfigManager(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    result = SzConfigManagerDict(sz_configmanager)
    return result


@pytest.fixture(name="sz_diagnostic", scope="module")
def szdiagnostic_fixture(engine_vars: Dict[Any, Any]) -> SzDiagnosticDict:
    """Single szdiagnostic object to use for all tests.
    engine_vars is returned from conftest.pys"""
    sz_diagnostic = SzDiagnostic(
        instance_name=engine_vars["INSTANCE_NAME"],
        settings=engine_vars["SETTINGS"],
        config_id=0,
        verbose_logging=0,
    )
    result = SzDiagnosticDict(sz_diagnostic)
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
