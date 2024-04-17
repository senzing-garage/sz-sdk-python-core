import pytest

from . import szhasher

# -----------------------------------------------------------------------------
# G2Hasher fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="g2hasher_instance", scope="module")
def g2hasher_instance_fixture(engine_vars):
    """
    Single engine object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    result = szhasher.G2Hasher(engine_vars["MODULE_NAME"], engine_vars["INI_PARAMS"])
    return result


# -----------------------------------------------------------------------------
# G2Hasher testcases
# -----------------------------------------------------------------------------


def test_process(g2hasher_instance):
    """Test Senzing license."""
    actual = g2hasher_instance.process("")
    assert isinstance(actual, str)
    assert actual == "response"
