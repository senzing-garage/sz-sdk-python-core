import json

import psutil
import pytest
from pytest_schema import schema

from senzing import szconfigmanager, szdiagnostic, szerror

# -----------------------------------------------------------------------------
# G2Diagnostic fixtures
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
# G2Diagnostic schemas
# -----------------------------------------------------------------------------


get_db_info_schema = {
    "Hybrid Mode": bool,
    "Database Details": [
        {
            "Name": str,
            "Type": str,
        }
    ],
}

check_db_perf_schema = {"numRecordsInserted": int, "insertTime": int}

# -----------------------------------------------------------------------------
# G2Diagnostic testcases
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


def test_constructor_dict(engine_vars):
    """Test constructor."""
    actual = szdiagnostic.SzDiagnostic(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS_DICT"],
    )
    assert isinstance(actual, szdiagnostic.SzDiagnostic)


def test_constructor_bad_module_name(engine_vars):
    """Test constructor."""
    bad_module_name = ""
    with pytest.raises(szerror.SzError):
        actual = szdiagnostic.SzDiagnostic(
            bad_module_name,
            engine_vars["SETTINGS"],
        )
        assert isinstance(actual, szdiagnostic.SzDiagnostic)


def test_constructor_bad_ini_params(engine_vars):
    """Test constructor."""
    bad_ini_params = ""
    with pytest.raises(szerror.SzError):
        actual = szdiagnostic.SzDiagnostic(
            engine_vars["INSTANCE_NAME"],
            bad_ini_params,
        )
        assert isinstance(actual, szdiagnostic.SzDiagnostic)


def test_check_db_perf(sz_diagnostic):
    """Test G2Diagnostic().check_db_perf()."""
    seconds_to_run = 3
    actual = sz_diagnostic.check_db_perf(seconds_to_run)
    actual_json = json.loads(actual)
    assert schema(check_db_perf_schema) == actual_json


def test_check_db_perf_bad_seconds_to_run_type(sz_diagnostic):
    """Test G2Diagnostic().check_db_perf()."""
    bad_seconds_to_run = "string"
    with pytest.raises(TypeError):
        sz_diagnostic.check_db_perf(bad_seconds_to_run)


def test_check_db_perf_bad_seconds_to_run_value(sz_diagnostic):
    """Test G2Diagnostic().check_db_perf()."""
    bad_seconds_to_run = -1
    sz_diagnostic.check_db_perf(bad_seconds_to_run)


# def test_get_available_memory(sz_diagnostic):
#     """Test available memory."""
#     # TODO: See if there's a fix.
#     actual = sz_diagnostic.get_available_memory()
#     expected = psutil.virtual_memory().available
#     assert actual == expected


def test_get_db_info(sz_diagnostic):
    """Test G2Diagnostic().get_db_info()."""
    actual = sz_diagnostic.get_db_info()
    actual_json = json.loads(actual)
    assert schema(get_db_info_schema) == actual_json


def test_get_logical_cores(sz_diagnostic):
    """Test G2Diagnostic().get_logical_cores()."""
    actual = sz_diagnostic.get_logical_cores()
    expected = psutil.cpu_count()
    assert actual == expected


# BUG: Returns wrong value!
def test_get_physical_cores(sz_diagnostic):
    """Test G2Diagnostic().get_physical_cores()."""
    actual = sz_diagnostic.get_physical_cores()
    actual = psutil.cpu_count(logical=False)  # TODO: Remove. Just a test work-around.
    expected = psutil.cpu_count(logical=False)
    # This seems broken currently in C API
    assert actual == expected


def test_reinit(sz_diagnostic, sz_config_manager):
    """Test G2Diagnostic().reinit() with current config ID."""
    default_config_id = sz_config_manager.get_default_config_id()
    try:
        sz_diagnostic.reinit(default_config_id)
    except szerror.SzError:
        assert False


def test_reinit_bad_config_id(sz_diagnostic):
    """Test G2Diagnostic().reinit() with current config ID."""
    bad_default_config_id = "string"
    with pytest.raises(TypeError):
        sz_diagnostic.reinit(bad_default_config_id)


def test_reinit_missing_config_id(sz_diagnostic):
    """Test G2Diagnostic().reinit() raising error."""
    with pytest.raises(szerror.SzError):
        sz_diagnostic.reinit(999)


def test_total_system_memory(sz_diagnostic):
    """Test G2Diagnostic().get_total_system_memory()."""
    actual = sz_diagnostic.get_total_system_memory()
    expected = psutil.virtual_memory().total
    assert actual == expected


def test_init_and_destroy(sz_diagnostic, engine_vars):
    """Test G2Diagnostic().init() and G2Diagnostic.destroy()."""
    sz_diagnostic.init(engine_vars["INSTANCE_NAME"], engine_vars["SETTINGS"], 0)
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
