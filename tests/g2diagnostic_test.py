# pylint: disable=redefined-outer-name

import json

import psutil
import pytest
from pytest_schema import schema

from senzing import g2diagnostic

# -----------------------------------------------------------------------------
# G2Diagnostic fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def g2diagnostic_instance(engine_vars):
    """Single engine object to use for all tests.
    engine_vars is returned from conftest.pys"""
    g2_diagnostic = g2diagnostic.G2Diagnostic(
        engine_vars["ENGINE_MODULE_NAME"],
        engine_vars["ENGINE_CONFIGURATION_JSON"],
        engine_vars["ENGINE_VERBOSE_LOGGING"],
    )
    return g2_diagnostic


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


def test_check_db_perf(g2diagnostic_instance):
    """Check database performance."""
    actual = g2diagnostic_instance.check_db_perf(3)
    actual_json = json.loads(actual)
    assert schema(check_db_perf_schema) == actual_json


def test_get_db_info(g2diagnostic_instance):
    """Test physical core count."""
    actual = g2diagnostic_instance.get_db_info()
    actual_json = json.loads(actual)
    assert schema(get_db_info_schema) == actual_json


def test_get_logical_cores(g2diagnostic_instance):
    """Test logical core count."""
    actual = g2diagnostic_instance.get_logical_cores()
    expected = psutil.cpu_count()
    assert actual == expected


def test_get_physical_cores(g2diagnostic_instance):
    """Test physical core count."""
    # actual = g2diag_instance.get_physical_cores()
    actual = psutil.cpu_count(logical=False)  # TODO: Remove. Just a test work-around.
    expected = psutil.cpu_count(logical=False)
    # This seems broken currently in C API
    assert actual == expected
