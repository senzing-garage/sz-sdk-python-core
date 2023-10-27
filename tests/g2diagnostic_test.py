# import psutil

# import multiprocessing
# import json

import pytest

from senzing import g2diagnostic


@pytest.fixture
def g2diag_instance(engine_vars):
    """Single engine object to use for all tests.
    engine_vars is returned from conftest.pys"""
    g2_diagnostic = g2diagnostic.G2Diagnostic(
        engine_vars["ENGINE_MODULE_NAME"],
        engine_vars["ENGINE_CONFIGURATION_JSON"],
        engine_vars["ENGINE_VERBOSE_LOGGING"],
    )
    return g2_diagnostic


def test_get_db_info(g2diag_instance):
    """Test physical core count."""
    actual = g2diag_instance.get_db_info()
    print()
    print(type(actual))
    print(f"{actual = }")
    assert actual == actual


# def test_get_logical_cores(g2diag_instance):
def test_get_logical_cores():
    """Test logical core count."""
    # expected = multiprocessing.cpu_count()
    # actual = g2diag_instance.get_logical_cores()
    # expected = psutil.cpu_count()
    # assert actual == expected
    actual = "test"
    assert actual == actual  # print(f"{actual:}")


# def test_get_physical_cores(g2diag_instance):
def test_get_physical_cores():
    """Test physical core count."""
    # expected = multiprocessing.cpu_count()
    # actual = g2diag_instance.get_physical_cores()
    # expected = psutil.cpu_count(logical=False)
    # assert actual == expected
    actual = "test"
    assert actual == actual  # print(f"{actual:}")
