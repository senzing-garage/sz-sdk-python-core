import pytest

from senzing import g2hasher

# -----------------------------------------------------------------------------
# G2Product fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="g2hasher_instance")
def g2hasher_instance_fixture(engine_vars):
    """
    Single engine object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    result = g2hasher.G2Hasher(
        engine_vars["MODULE_NAME"],
        engine_vars["INI_PARAMS"],
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
