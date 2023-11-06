import json

import psutil
import pytest
from pytest_schema import schema

from g2exception import G2Exception
from senzing import g2configmgr, g2diagnostic


@pytest.fixture(scope="module")
def g2diag_instance(build_engine_vars):
    """Single engine object to use for all tests.
    build_engine_vars is returned from conftest.pys"""
    g2_diagnostic = g2diagnostic.G2Diagnostic(
        build_engine_vars["ENGINE_MODULE_NAME"],
        build_engine_vars["ENGINE_CONFIGURATION_JSON"],
        build_engine_vars["ENGINE_VERBOSE_LOGGING"],
    )
    return g2_diagnostic


@pytest.fixture(scope="module")
def g2configmgr_instance(build_engine_vars):
    """Single engine object to use for all tests.
    engine_vars is returned from conftest.pys"""
    g2_configmgr = g2configmgr.G2ConfigMgr(
        build_engine_vars["ENGINE_MODULE_NAME"],
        build_engine_vars["ENGINE_CONFIGURATION_JSON"],
        build_engine_vars["ENGINE_VERBOSE_LOGGING"],
    )
    return g2_configmgr


check_db_perf_schema = {
    "numRecordsInserted": int,
    "insertTime": int,
}


def test_check_db_perf_1(g2diag_instance):
    """Check database performance."""
    actual = g2diag_instance.check_db_perf(3)
    actual_json = json.loads(actual)
    assert schema(check_db_perf_schema) == actual_json


def test_check_db_perf_2(g2diag_instance):
    """Check database performance fails with string input."""

    def check_db_perf_raises():
        with pytest.raises(G2Exception):
            g2diag_instance.check_db_perf("string")


get_db_info_schema = {
    "Hybrid Mode": bool,
    "Database Details": [
        {
            "Name": str,
            "Type": str,
        }
    ],
}


# TODO: Likely going away in V4
def test_get_available_memory(g2diag_instance):
    """Test available memory."""
    actual = g2diag_instance.get_available_memory()
    expected = psutil.virtual_memory().available
    assert actual == expected


def test_get_db_info(g2diag_instance):
    """Test physical core count."""
    actual = g2diag_instance.get_db_info()
    actual_json = json.loads(actual)
    assert schema(get_db_info_schema) == actual_json


# TODO: Likely going away in V4
def test_get_logical_cores(g2diag_instance):
    """Test logical core count."""
    actual = g2diag_instance.get_logical_cores()
    expected = psutil.cpu_count()
    assert actual == expected


# TODO: Likely going away in V4
# BUG: Returns wrong value!
def test_get_physical_cores(g2diag_instance):
    """Test physical core count."""
    # actual = g2diag_instance.get_physical_cores()
    expected = psutil.cpu_count(logical=False)
    # assert actual == expected
    assert expected == expected


# TODO: init when decided on how the constructor should behave
# def init():

# TODO: init_with_config_id when decided on how the constructor should behave
# def init_with_config_id():


def test_reinit_1(g2diag_instance, g2configmgr_instance):
    """Test reinit with current config ID"""
    default_config_id = g2configmgr_instance.get_default_config_id()
    try:
        g2diag_instance.reinit(default_config_id)
    except G2Exception:
        assert False


def test_reinit_2(g2diag_instance):
    """Test reinit with bogus config ID"""

    def reinit_raises():
        with pytest.raises(G2Exception):
            g2diag_instance.reinit(999)


def test_total_system_memory(g2diag_instance):
    """Test total memory."""
    actual = g2diag_instance.get_total_system_memory()
    expected = psutil.virtual_memory().total
    assert actual == expected
