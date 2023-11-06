import pytest

from senzing import g2configmgr


@pytest.fixture(scope="module")
def g2configmgr_instance(build_engine_vars):
    """Single engine object to use for all tests.
    build_engine_vars is returned from conftest.pys"""
    g2_configmgr = g2configmgr.G2ConfigMgr(
        build_engine_vars["ENGINE_MODULE_NAME"],
        build_engine_vars["ENGINE_CONFIGURATION_JSON"],
        build_engine_vars["ENGINE_VERBOSE_LOGGING"],
    )
    return g2_configmgr


def test_get_default_config_id(g2configmgr_instance):
    """Test get_default_config_id"""
    default_config_id = g2configmgr_instance.get_default_config_id()
    assert isinstance(default_config_id, int)
