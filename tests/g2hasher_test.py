# pylint: disable=redefined-outer-name


import pytest

from senzing import g2hasher

# -----------------------------------------------------------------------------
# G2Product fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def g2hasher_instance(engine_vars):
    """
    Single engine object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    result = g2hasher.G2Hasher(
        engine_vars["ENGINE_MODULE_NAME"],
        engine_vars["ENGINE_CONFIGURATION_JSON"],
        0,
    )
    return result


# -----------------------------------------------------------------------------
# G2Hasher testcases
# -----------------------------------------------------------------------------


def test_process(g2hasher_instance):
    """Test Senzing license."""
    actual = g2hasher_instance.process("")
    assert isinstance(actual, str)
    assert actual == "response"
