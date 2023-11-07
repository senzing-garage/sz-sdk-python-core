import pytest

from senzing import g2configmgr


@pytest.fixture(name="g2configmgr_instance", scope="module")
def g2configmgr_instance_fixture(engine_vars):
    """Single engine object to use for all tests.
    build_engine_vars is returned from conftest.pys"""
    result = g2configmgr.G2ConfigMgr(
        engine_vars["MODULE_NAME"],
        engine_vars["INI_PARAMS"],
    )
    return result


def test_get_default_config_id(g2configmgr_instance):
    """Test get_default_config_id"""
    default_config_id = g2configmgr_instance.get_default_config_id()
    assert isinstance(default_config_id, int)
