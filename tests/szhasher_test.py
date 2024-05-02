import pytest

from senzing import szhasher

# -----------------------------------------------------------------------------
# SzHasher fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="szhasher_instance", scope="module")
def szhasher_instance_fixture(engine_vars):
    """
    Single engine object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    result = szhasher.SzHasher(engine_vars["INSTANCE_NAME"], engine_vars["SETTINGS"])
    return result


# -----------------------------------------------------------------------------
# SzHasher testcases
# -----------------------------------------------------------------------------


def test_process(szhasher_instance):
    """Test Senzing license."""
    actual = szhasher_instance.process("")
    assert isinstance(actual, str)
    assert actual == "response"
