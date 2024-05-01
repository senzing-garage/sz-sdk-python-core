import json
from ctypes import ArgumentError

import pytest
from pytest_schema import schema

from senzing import SzError, szconfigmanager, szdiagnostic

# -----------------------------------------------------------------------------
# SzDiagnostic testcases
# -----------------------------------------------------------------------------


def test_exception(sz_diagnostic) -> None:
    """Test exceptions."""
    actual = sz_diagnostic.new_exception(0)
    assert isinstance(actual, Exception)


def test_constructor(engine_vars) -> None:
    """Test constructor."""
    actual = szdiagnostic.SzDiagnostic(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    assert isinstance(actual, szdiagnostic.SzDiagnostic)


def test_constructor_dict(engine_vars) -> None:
    """Test constructor."""
    actual = szdiagnostic.SzDiagnostic(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS_DICT"],
    )
    assert isinstance(actual, szdiagnostic.SzDiagnostic)


def test_constructor_bad_instance_name(engine_vars) -> None:
    """Test constructor."""
    bad_instance_name = ""
    with pytest.raises(SzError):
        actual = szdiagnostic.SzDiagnostic(
            bad_instance_name,
            engine_vars["SETTINGS"],
        )
        assert isinstance(actual, szdiagnostic.SzDiagnostic)


def test_constructor_bad_settings(engine_vars) -> None:
    """Test constructor."""
    bad_settings = ""
    with pytest.raises(SzError):
        actual = szdiagnostic.SzDiagnostic(
            engine_vars["INSTANCE_NAME"],
            bad_settings,
        )
        assert isinstance(actual, szdiagnostic.SzDiagnostic)


def test_check_datastore_performance(sz_diagnostic: szdiagnostic.SzDiagnostic) -> None:
    """Test SzDiagnostic().check_datastore_performance()."""
    seconds_to_run = 3
    actual = sz_diagnostic.check_datastore_performance(seconds_to_run)
    actual_json = json.loads(actual)
    assert schema(check_datastore_performance_schema) == actual_json


def test_check_datastore_performance_bad_seconds_to_run_type(
    sz_diagnostic: szdiagnostic.SzDiagnostic,
) -> None:
    """Test SzDiagnostic().check_datastore_performance()."""
    bad_seconds_to_run = "string"
    with pytest.raises(ArgumentError):
        sz_diagnostic.check_datastore_performance(bad_seconds_to_run)  # type: ignore[arg-type]


def test_check_datastore_performance_bad_seconds_to_run_value(
    sz_diagnostic: szdiagnostic.SzDiagnostic,
) -> None:
    """Test SzDiagnostic().check_datastore_performance()."""
    bad_seconds_to_run = -1
    sz_diagnostic.check_datastore_performance(bad_seconds_to_run)


def test_get_datastore_info(sz_diagnostic: szdiagnostic.SzDiagnostic) -> None:
    """Test SzDiagnostic().get_datastore_info()."""
    actual = sz_diagnostic.get_datastore_info()
    actual_json = json.loads(actual)
    assert schema(get_datastore_info_schema) == actual_json


def test_reinitialize(
    sz_diagnostic: szdiagnostic.SzDiagnostic, sz_config_manager
) -> None:
    """Test SzDiagnostic().reinit() with current config ID."""
    default_config_id = sz_config_manager.get_default_config_id()
    try:
        sz_diagnostic.reinitialize(default_config_id)
    except SzError:
        assert False


def test_reinitialize_bad_config_id(sz_diagnostic: szdiagnostic.SzDiagnostic) -> None:
    """Test SzDiagnostic().reinit() with current config ID."""
    bad_default_config_id = "string"
    with pytest.raises(ArgumentError):
        sz_diagnostic.reinitialize(bad_default_config_id)  # type: ignore[arg-type]


def test_reinitialize_missing_config_id(
    sz_diagnostic: szdiagnostic.SzDiagnostic,
) -> None:
    """Test SzDiagnostic().reinit() raising error."""
    with pytest.raises(SzError):
        sz_diagnostic.reinitialize(999)


def test_initialize_and_destroy(
    sz_diagnostic: szdiagnostic.SzDiagnostic, engine_vars
) -> None:
    """Test SzDiagnostic().init() and SzDiagnostic.destroy()."""
    sz_diagnostic.initialize(engine_vars["INSTANCE_NAME"], engine_vars["SETTINGS"], 0)
    sz_diagnostic.destroy()


# TODO: Uncomment testcase after Senzing code build 2024_05_01__07_22.
# def test_init_and_destroy_again(sz_diagnostic, engine_vars):
#     """Test SzDiagnostic().init() and SzDiagnostic.destroy()."""
#     sz_diagnostic.initialize(engine_vars["INSTANCE_NAME"], engine_vars["SETTINGS"], 0)
#     sz_diagnostic.destroy()


# TODO: Uncomment testcase after Senzing code build 2024_05_01__07_22.
# def test_initialize_with_config_id_and_destroy(sz_config_manager, engine_vars):
#     """Test SzDiagnostic().init_with_config_id() and SzDiagnostic.destroy()."""
#     # TODO: This has the same issue as test_init_and_destroy_2
#     default_config_id = sz_config_manager.get_default_config_id()
#     sz_diagnostic = szdiagnostic.SzDiagnostic()
#     sz_diagnostic.initialize(
#         instance_name=engine_vars["INSTANCE_NAME"],
#         settings=engine_vars["SETTINGS"],
#         config_id=default_config_id,
#         verbose_logging=0,
#     )
#     sz_diagnostic.destroy()


# TODO: Uncomment testcase after Senzing code build 2024_05_01__07_22.
# def test_context_managment(engine_vars) -> None:
#     """Test the use of SzDiagnostic in context."""
#     with szdiagnostic.SzDiagnostic(
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


@pytest.fixture(name="sz_config_manager", scope="module")
def szconfigmanager_fixture(engine_vars):
    """Single engine object to use for all tests.
    engine_vars is returned from conftest.pys"""
    result = szconfigmanager.SzConfigManager(
        instance_name=engine_vars["INSTANCE_NAME"],
        settings=engine_vars["SETTINGS"],
        verbose_logging=0,
    )
    return result


@pytest.fixture(name="sz_diagnostic", scope="module")
def szdiagnostic_fixture(engine_vars):
    """Single engine object to use for all tests.
    engine_vars is returned from conftest.pys"""
    result = szdiagnostic.SzDiagnostic(
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