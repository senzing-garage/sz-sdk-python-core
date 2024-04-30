import json
from ctypes import ArgumentError

import pytest
from pytest_schema import schema

from senzing import szconfigmanager, szdiagnostic, szerror

# -----------------------------------------------------------------------------
# SzDiagnostic testcases
# -----------------------------------------------------------------------------


def test_exception(sz_diagnostic):
    """Test exceptions."""
    actual = sz_diagnostic.new_exception(0)
    assert isinstance(actual, Exception)


def test_constructor(engine_vars):
    """Test constructor."""
    actual = szdiagnostic.SzDiagnostic(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    assert isinstance(actual, szdiagnostic.SzDiagnostic)


# def test_constructor2(engine_vars):
#     """Test constructor."""
#     actual = szdiagnostic.SzDiagnostic(
#         engine_vars["INSTANCE_NAME"],
#         engine_vars["SETTINGS"],
#     )
#     assert isinstance(actual, szdiagnostic.SzDiagnostic)


# def test_constructor_dict(engine_vars):
#     """Test constructor."""
#     actual = szdiagnostic.SzDiagnostic(
#         engine_vars["INSTANCE_NAME"],
#         engine_vars["SETTINGS_DICT"],
#     )
#     assert isinstance(actual, szdiagnostic.SzDiagnostic)


# def test_constructor_bad_instance_name(engine_vars):
#     """Test constructor."""
#     bad_module_name = ""
#     with pytest.raises(szerror.SzError):
#         actual = szdiagnostic.SzDiagnostic(
#             bad_module_name,
#             engine_vars["SETTINGS"],
#         )
#         assert isinstance(actual, szdiagnostic.SzDiagnostic)


# def test_constructor_bad_settings(engine_vars):
#     """Test constructor."""
#     bad_ini_params = ""
#     with pytest.raises(szerror.SzError):
#         actual = szdiagnostic.SzDiagnostic(
#             engine_vars["INSTANCE_NAME"],
#             bad_ini_params,
#         )
#         assert isinstance(actual, szdiagnostic.SzDiagnostic)


def test_check_datastore_performance(sz_diagnostic):
    """Test G2Diagnostic().check_db_perf()."""
    seconds_to_run = 3
    actual = sz_diagnostic.check_datastore_performance(seconds_to_run)
    actual_json = json.loads(actual)
    assert schema(check_datastore_performance_schema) == actual_json


def test_check_datastore_performance_bad_seconds_to_run_type(sz_diagnostic):
    """Test G2Diagnostic().check_db_perf()."""
    bad_seconds_to_run = "string"
    with pytest.raises(ArgumentError):
        sz_diagnostic.check_datastore_performance(bad_seconds_to_run)


def test_check_datastore_performance_bad_seconds_to_run_value(sz_diagnostic):
    """Test G2Diagnostic().check_db_perf()."""
    bad_seconds_to_run = -1
    sz_diagnostic.check_datastore_performance(bad_seconds_to_run)


def test_get_datastore_info(sz_diagnostic):
    """Test G2Diagnostic().get_db_info()."""
    actual = sz_diagnostic.get_datastore_info()
    actual_json = json.loads(actual)
    assert schema(get_datastore_info_schema) == actual_json


def test_reinitialize(sz_diagnostic, sz_config_manager):
    """Test G2Diagnostic().reinit() with current config ID."""
    default_config_id = sz_config_manager.get_default_config_id()
    try:
        sz_diagnostic.reinitialize(default_config_id)
    except szerror.SzError:
        assert False


def test_reinitialize_bad_config_id(sz_diagnostic):
    """Test G2Diagnostic().reinit() with current config ID."""
    bad_default_config_id = "string"
    with pytest.raises(ArgumentError):
        sz_diagnostic.reinitialize(bad_default_config_id)


def test_reinitialize_missing_config_id(sz_diagnostic):
    """Test G2Diagnostic().reinit() raising error."""
    with pytest.raises(szerror.SzError):
        sz_diagnostic.reinitialize(999)


def test_initialize_and_destroy(sz_diagnostic, engine_vars):
    """Test G2Diagnostic().init() and G2Diagnostic.destroy()."""
    sz_diagnostic.initialize(engine_vars["INSTANCE_NAME"], engine_vars["SETTINGS"], 0)
    sz_diagnostic.destroy()


# def test_init_and_destroy_again(sz_diagnostic, engine_vars):
#     """Test G2Diagnostic().init() and G2Diagnostic.destroy()."""
#     # TODO: Doesn't work
#     sz_diagnostic.init(engine_vars["INSTANCE_NAME"], engine_vars["SETTINGS"], 0)
#     sz_diagnostic.destroy()


# def test_init_with_config_id_and_destroy(sz_config_manager, engine_vars):
#     """Test G2Diagnostic().init_with_config_id() and G2Diagnostic.destroy()."""
#     # TODO: This has the same issue as test_init_and_destroy_2
#     default_config_id = sz_config_manager.get_default_config_id()
#     sz_diagnostic_2 = g2diagnostic.G2Diagnostic()
#     sz_diagnostic_2.init_with_config_id(
#         engine_vars["INSTANCE_NAME"], engine_vars["SETTINGS"], default_config_id, 0
#     )
#     sz_diagnostic_2.destroy()


# def test_context_managment(engine_vars) -> None:
#     """Test the use of SzDiagnosticGrpc in context."""
#     with szdiagnostic.SzDiagnostic(
#         engine_vars["INSTANCE_NAME"],
#         engine_vars["SETTINGS"],
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
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    return result


@pytest.fixture(name="sz_diagnostic", scope="module")
def szdiagnostic_fixture(engine_vars):
    """Single engine object to use for all tests.
    engine_vars is returned from conftest.pys"""
    result = szdiagnostic.SzDiagnostic(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
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
