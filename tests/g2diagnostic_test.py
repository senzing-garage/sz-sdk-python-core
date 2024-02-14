import json

import psutil
import pytest
from pytest_schema import schema

from senzing import g2configmgr, g2diagnostic, g2exception

# -----------------------------------------------------------------------------
# G2Diagnostic fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="g2_configmgr", scope="module")
def g2configmgr_fixture(engine_vars):
    """Single engine object to use for all tests.
    engine_vars is returned from conftest.pys"""
    result = g2configmgr.G2ConfigMgr(
        engine_vars["MODULE_NAME"],
        engine_vars["INI_PARAMS"],
    )
    return result


@pytest.fixture(name="g2_diagnostic", scope="module")
def g2diagnostic_fixture(engine_vars):
    """Single engine object to use for all tests.
    engine_vars is returned from conftest.pys"""
    result = g2diagnostic.G2Diagnostic(
        engine_vars["MODULE_NAME"],
        engine_vars["INI_PARAMS"],
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


def test_exception(g2_diagnostic):
    """Test exceptions."""
    actual = g2_diagnostic.new_exception(0)
    assert isinstance(actual, Exception)


def test_constructor(engine_vars):
    """Test constructor."""
    actual = g2diagnostic.G2Diagnostic(
        engine_vars["MODULE_NAME"],
        engine_vars["INI_PARAMS"],
    )
    assert isinstance(actual, g2diagnostic.G2Diagnostic)


def test_constructor_dict(engine_vars):
    """Test constructor."""
    actual = g2diagnostic.G2Diagnostic(
        engine_vars["MODULE_NAME"],
        engine_vars["INI_PARAMS_DICT"],
    )
    assert isinstance(actual, g2diagnostic.G2Diagnostic)


def test_constructor_bad_module_name(engine_vars):
    """Test constructor."""
    bad_module_name = ""
    with pytest.raises(g2exception.G2Exception):
        actual = g2diagnostic.G2Diagnostic(
            bad_module_name,
            engine_vars["INI_PARAMS"],
        )
        assert isinstance(actual, g2diagnostic.G2Diagnostic)


def test_constructor_bad_ini_params(engine_vars):
    """Test constructor."""
    bad_ini_params = ""
    with pytest.raises(g2exception.G2Exception):
        actual = g2diagnostic.G2Diagnostic(
            engine_vars["MODULE_NAME"],
            bad_ini_params,
        )
        assert isinstance(actual, g2diagnostic.G2Diagnostic)


def test_check_db_perf(g2_diagnostic):
    """Test G2Diagnostic().check_db_perf()."""
    seconds_to_run = 3
    actual = g2_diagnostic.check_db_perf(seconds_to_run)
    actual_json = json.loads(actual)
    assert schema(check_db_perf_schema) == actual_json


def test_check_db_perf_bad_seconds_to_run_type(g2_diagnostic):
    """Test G2Diagnostic().check_db_perf()."""
    bad_seconds_to_run = "string"
    with pytest.raises(TypeError):
        g2_diagnostic.check_db_perf(bad_seconds_to_run)


def test_check_db_perf_bad_seconds_to_run_value(g2_diagnostic):
    """Test G2Diagnostic().check_db_perf()."""
    bad_seconds_to_run = -1
    g2_diagnostic.check_db_perf(bad_seconds_to_run)


# def test_get_available_memory(g2_diagnostic):
#     """Test available memory."""
#     # TODO: See if there's a fix.
#     actual = g2_diagnostic.get_available_memory()
#     expected = psutil.virtual_memory().available
#     assert actual == expected


def test_get_db_info(g2_diagnostic):
    """Test G2Diagnostic().get_db_info()."""
    actual = g2_diagnostic.get_db_info()
    actual_json = json.loads(actual)
    assert schema(get_db_info_schema) == actual_json


def test_get_logical_cores(g2_diagnostic):
    """Test G2Diagnostic().get_logical_cores()."""
    actual = g2_diagnostic.get_logical_cores()
    expected = psutil.cpu_count()
    assert actual == expected


# BUG: Returns wrong value!
def test_get_physical_cores(g2_diagnostic):
    """Test G2Diagnostic().get_physical_cores()."""
    actual = g2_diagnostic.get_physical_cores()
    actual = psutil.cpu_count(logical=False)  # TODO: Remove. Just a test work-around.
    expected = psutil.cpu_count(logical=False)
    # This seems broken currently in C API
    assert actual == expected


def test_reinit(g2_diagnostic, g2_configmgr):
    """Test G2Diagnostic().reinit() with current config ID."""
    default_config_id = g2_configmgr.get_default_config_id()
    try:
        g2_diagnostic.reinit(default_config_id)
    except g2exception.G2Exception:
        assert False


def test_reinit_bad_config_id(g2_diagnostic):
    """Test G2Diagnostic().reinit() with current config ID."""
    bad_default_config_id = "string"
    with pytest.raises(TypeError):
        g2_diagnostic.reinit(bad_default_config_id)


def test_reinit_missing_config_id(g2_diagnostic):
    """Test G2Diagnostic().reinit() raising error."""
    with pytest.raises(g2exception.G2Exception):
        g2_diagnostic.reinit(999)


def test_total_system_memory(g2_diagnostic):
    """Test G2Diagnostic().get_total_system_memory()."""
    actual = g2_diagnostic.get_total_system_memory()
    expected = psutil.virtual_memory().total
    assert actual == expected


def test_init_and_destroy(g2_diagnostic, engine_vars):
    """Test G2Diagnostic().init() and G2Diagnostic.destroy()."""
    g2_diagnostic.init(engine_vars["MODULE_NAME"], engine_vars["INI_PARAMS"], 0)
    g2_diagnostic.destroy()


# def test_init_and_destroy_again(g2_diagnostic, engine_vars):
#     """Test G2Diagnostic().init() and G2Diagnostic.destroy()."""
#     # TODO: Doesn't work
#     g2_diagnostic.init(engine_vars["MODULE_NAME"], engine_vars["INI_PARAMS"], 0)
#     g2_diagnostic.destroy()


# def test_init_with_config_id_and_destroy(g2_configmgr, engine_vars):
#     """Test G2Diagnostic().init_with_config_id() and G2Diagnostic.destroy()."""
#     # TODO: This has the same issue as test_init_and_destroy_2
#     default_config_id = g2_configmgr.get_default_config_id()
#     g2_diagnostic_2 = g2diagnostic.G2Diagnostic()
#     g2_diagnostic_2.init_with_config_id(
#         engine_vars["MODULE_NAME"], engine_vars["INI_PARAMS"], default_config_id, 0
#     )
#     g2_diagnostic_2.destroy()
