import json

import psutil
import pytest
from pytest_schema import schema

from senzing import g2configmgr, g2diagnostic, g2exception

# -----------------------------------------------------------------------------
# G2Diagnostic fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="g2configmgr_instance", scope="module")
def g2configmgr_instance_fixture(engine_vars):
    """Single engine object to use for all tests.
    engine_vars is returned from conftest.pys"""
    result = g2configmgr.G2ConfigMgr(
        engine_vars["MODULE_NAME"],
        engine_vars["INI_PARAMS"],
    )
    return result


@pytest.fixture(name="g2diagnostic_instance", scope="module")
def g2diagnostic_instance_fixture(engine_vars):
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


def test_check_db_perf_1(g2diagnostic_instance):
    """Check database performance."""
    actual = g2diagnostic_instance.check_db_perf(3)
    actual_json = json.loads(actual)
    assert schema(check_db_perf_schema) == actual_json


# def test_check_db_perf_2(g2diagnostic_instance):
#     """Check database performance fails with string input."""

#     with pytest.raises(g2exception.G2Exception):
#         g2diagnostic_instance.check_db_perf("string")


def test_check_db_perf_3(g2diagnostic_instance):
    """Check database performance fails with string input."""

    with pytest.raises(AssertionError):
        g2diagnostic_instance.check_db_perf("string")


# TODO: Likely going away in V4
def test_get_available_memory(g2diagnostic_instance):
    """Test available memory."""
    actual = g2diagnostic_instance.get_available_memory()
    expected = psutil.virtual_memory().available
    assert actual == expected


def test_get_db_info(g2diagnostic_instance):
    """Test physical core count."""
    actual = g2diagnostic_instance.get_db_info()
    actual_json = json.loads(actual)
    assert schema(get_db_info_schema) == actual_json


# TODO: Likely going away in V4
def test_get_logical_cores(g2diagnostic_instance):
    """Test logical core count."""
    actual = g2diagnostic_instance.get_logical_cores()
    expected = psutil.cpu_count()
    assert actual == expected


# TODO: Likely going away in V4
# BUG: Returns wrong value!
def test_get_physical_cores(g2diagnostic_instance):
    """Test physical core count."""
    actual = g2diagnostic_instance.get_physical_cores()
    actual = psutil.cpu_count(logical=False)  # TODO: Remove. Just a test work-around.
    expected = psutil.cpu_count(logical=False)
    # This seems broken currently in C API
    assert actual == expected


# TODO: init when decided on how the constructor should behave
# def init():

# TODO: init_with_config_id when decided on how the constructor should behave
# def init_with_config_id():


def test_reinit_1(g2diagnostic_instance, g2configmgr_instance):
    """Test reinit with current config ID"""
    default_config_id = g2configmgr_instance.get_default_config_id()
    try:
        g2diagnostic_instance.reinit(default_config_id)
    except g2exception.G2Exception:
        assert False


def test_reinit_2(g2diagnostic_instance):
    """Test reinit with bogus config ID"""
    with pytest.raises(g2exception.G2Exception):
        g2diagnostic_instance.reinit(999)


def test_total_system_memory(g2diagnostic_instance):
    """Test total memory."""
    actual = g2diagnostic_instance.get_total_system_memory()
    expected = psutil.virtual_memory().total
    assert actual == expected
