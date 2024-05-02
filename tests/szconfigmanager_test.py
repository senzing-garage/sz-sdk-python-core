import json
from ctypes import ArgumentError
from typing import Any, Dict

import pytest
from pytest_schema import Optional, Or, schema
from senzing_truthset import TRUTHSET_DATASOURCES

from senzing import (
    SzConfig,
    SzConfigManager,
    SzConfigurationError,
    SzEngineFlags,
    SzError,
)

# -----------------------------------------------------------------------------
# SzConfigManager testcases
# -----------------------------------------------------------------------------


def test_exception(sz_configmanager: SzConfigManager) -> None:
    """Test exceptions."""
    actual = sz_configmanager.new_exception(0)
    assert isinstance(actual, Exception)


def test_constructor(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    actual = SzConfigManager(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    assert isinstance(actual, SzConfigManager)


def test_constructor_dict(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    actual = SzConfigManager(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS_DICT"],
    )
    assert isinstance(actual, SzConfigManager)


def test_constructor_bad_instance_name(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    bad_instance_name = ""
    with pytest.raises(SzError):
        actual = SzConfigManager(
            bad_instance_name,
            engine_vars["SETTINGS"],
        )
        assert isinstance(actual, SzConfigManager)


def test_constructor_bad_settings(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    bad_settings = ""
    with pytest.raises(SzError):
        actual = SzConfigManager(
            engine_vars["INSTANCE_NAME"],
            bad_settings,
        )
        assert isinstance(actual, SzConfigManager)


def test_add_config(sz_configmanager: SzConfigManager, sz_config: SzConfig) -> None:
    """Test SzConfigManager().add_config()."""
    config_handle = sz_config.create_config()
    config_definition = sz_config.export_config(config_handle)
    config_comment = "Test"
    actual = sz_configmanager.add_config(config_definition, config_comment)
    assert isinstance(actual, int)
    assert actual > 0


def test_add_config_dict(
    sz_configmanager: SzConfigManager, sz_config: SzConfig
) -> None:
    """Test SzConfigManager().add_config()."""
    config_handle = sz_config.create_config()
    config_definition = sz_config.export_config(config_handle)
    config_definition_dict = json.loads(config_definition)
    config_comment = "Test"
    actual = sz_configmanager.add_config(config_definition_dict, config_comment)
    assert isinstance(actual, int)
    assert actual > 0


def test_add_config_bad_config_definition_type(
    sz_configmanager: SzConfigManager,
) -> None:
    """Test SzConfigManager().add_config()."""
    bad_config_definition = 0
    config_comment = "Test"
    with pytest.raises(TypeError):
        sz_configmanager.add_config(
            bad_config_definition, config_comment  # type: ignore[arg-type]
        )


def test_add_config_bad_config_definition_value(
    sz_configmanager: SzConfigManager,
) -> None:
    """Test SzConfigManager().add_config()."""
    bad_config_definition = '{"just": "junk"}'
    config_comment = "Test"
    actual = sz_configmanager.add_config(bad_config_definition, config_comment)
    assert isinstance(actual, int)
    assert actual > 0


def test_add_config_bad_config_comment_type(
    sz_configmanager: SzConfigManager, sz_config: SzConfig
) -> None:
    """Test SzConfigManager().add_config()."""
    config_handle = sz_config.create_config()
    config_definition = sz_config.export_config(config_handle)
    bad_config_comment = 0
    with pytest.raises(TypeError):
        sz_configmanager.add_config(
            config_definition, bad_config_comment  # type: ignore[arg-type]
        )


def test_get_config(sz_configmanager: SzConfigManager) -> None:
    """Test SzConfigManager().get_default_config_id()."""
    config_id = sz_configmanager.get_default_config_id()
    actual = sz_configmanager.get_config(config_id)
    actual_json = json.loads(actual)
    assert schema(config_schema) == actual_json


def test_get_config_bad_config_id_type(
    sz_configmanager: SzConfigManager,
) -> None:
    """Test SzConfigManager().get_default_config_id()."""
    bad_config_id = "string"
    with pytest.raises(ArgumentError):
        sz_configmanager.get_config(bad_config_id)  # type: ignore[arg-type]


def test_get_config_bad_config_id_value(
    sz_configmanager: SzConfigManager,
) -> None:
    """Test SzConfigManager().get_default_config_id()."""
    bad_config_id = 1234
    with pytest.raises(SzConfigurationError):
        sz_configmanager.get_config(bad_config_id)


def test_get_config_list(sz_configmanager: SzConfigManager) -> None:
    """Test SzConfigManager().get_default_config_id()."""
    actual = sz_configmanager.get_config_list()
    actual_json = json.loads(actual)
    assert schema(config_list_schema) == actual_json


def test_get_default_config_id(
    sz_configmanager: SzConfigManager,
) -> None:
    """Test SzConfigManager().get_default_config_id()."""
    actual = sz_configmanager.get_default_config_id()
    assert isinstance(actual, int)


def test_replace_default_config_id(
    sz_configmanager: SzConfigManager, sz_config: SzConfig
) -> None:
    """Test SzConfigManager().get_default_config_id()."""
    current_default_config_id = sz_configmanager.get_default_config_id()
    config_handle = sz_config.create_config()
    for data_source_code in TRUTHSET_DATASOURCES:
        sz_config.add_data_source(config_handle, data_source_code)
    data_source_code = "REPLACE_DEFAULT_CONFIG_ID"
    sz_config.add_data_source(config_handle, data_source_code)
    config_definition = sz_config.export_config(config_handle)
    config_comment = "Test"
    new_default_config_id = sz_configmanager.add_config(
        config_definition, config_comment
    )
    assert current_default_config_id != new_default_config_id
    sz_configmanager.replace_default_config_id(
        current_default_config_id, new_default_config_id
    )
    actual = sz_configmanager.get_default_config_id()
    assert actual == new_default_config_id


def test_replace_default_config_id_bad_new_id_type(
    sz_configmanager: SzConfigManager,
) -> None:
    """Test SzConfigManager().get_default_config_id()."""
    current_default_config_id = sz_configmanager.get_default_config_id()
    bad_new_default_config_id = "string"
    with pytest.raises(ArgumentError):
        sz_configmanager.replace_default_config_id(
            current_default_config_id, bad_new_default_config_id  # type: ignore[arg-type]
        )


def test_replace_default_config_id_bad_new_id_value(
    sz_configmanager: SzConfigManager,
) -> None:
    """Test SzConfigManager().get_default_config_id()."""
    current_default_config_id = sz_configmanager.get_default_config_id()
    bad_new_default_config_id = 1234
    with pytest.raises(SzConfigurationError):
        sz_configmanager.replace_default_config_id(
            current_default_config_id, bad_new_default_config_id
        )


def test_replace_default_config_id_bad_current_default_config_id_type(
    sz_configmanager: SzConfigManager,
    sz_config: SzConfig,
) -> None:
    """Test SzConfigManager().get_default_config_id()."""
    bad_current_default_config_id = "string"
    config_handle = sz_config.create_config()
    data_source_code = "REPLACE_DEFAULT_CONFIG_ID"
    sz_config.add_data_source(config_handle, data_source_code)
    config_definition = sz_config.export_config(config_handle)
    config_comment = "Test"
    new_default_config_id = sz_configmanager.add_config(
        config_definition, config_comment
    )
    with pytest.raises(ArgumentError):
        sz_configmanager.replace_default_config_id(
            bad_current_default_config_id, new_default_config_id  # type: ignore[arg-type]
        )


def test_replace_default_config_id_bad_current_default_config_id_value(
    sz_configmanager: SzConfigManager,
    sz_config: SzConfig,
) -> None:
    """Test SzConfigManager().get_default_config_id()."""
    bad_current_default_config_id = 1234
    config_handle = sz_config.create_config()
    data_source_code = "CUSTOMERS"
    sz_config.add_data_source(config_handle, data_source_code)
    config_definition = sz_config.export_config(config_handle)
    config_comment = "Test"
    new_default_config_id = sz_configmanager.add_config(
        config_definition, config_comment
    )
    with pytest.raises(SzConfigurationError):
        sz_configmanager.replace_default_config_id(
            bad_current_default_config_id, new_default_config_id
        )


def test_set_default_config_id(
    sz_configmanager: SzConfigManager,
    sz_config: SzConfig,
) -> None:
    """Test SzConfigManager().get_default_config_id()."""
    old_config_id = sz_configmanager.get_default_config_id()
    config_handle = sz_config.create_config()
    data_source_code = "CUSTOMERS"
    sz_config.add_data_source(config_handle, data_source_code)
    config_definition = sz_config.export_config(config_handle)
    config_comment = "Test"
    config_id = sz_configmanager.add_config(config_definition, config_comment)
    assert old_config_id != config_id
    sz_configmanager.set_default_config_id(config_id)
    actual = sz_configmanager.get_default_config_id()
    assert actual == config_id


def test_set_default_config_id_bad_config_id_type(
    sz_configmanager: SzConfigManager,
) -> None:
    """Test SzConfigManager().get_default_config_id()."""
    bad_config_id = "string"
    with pytest.raises(ArgumentError):
        sz_configmanager.set_default_config_id(bad_config_id)  # type: ignore[arg-type]


def test_set_default_config_id_bad_config_id_value(
    sz_configmanager: SzConfigManager,
) -> None:
    """Test SzConfigManager().set_default_config_id()."""
    bad_config_id = 1
    with pytest.raises(SzConfigurationError):
        sz_configmanager.set_default_config_id(bad_config_id)


def test_initialize_and_destroy(
    sz_configmanager: SzConfigManager,
) -> None:
    """Test SzConfigManager().initialize() and SzConfigManager.destroy()."""
    instance_name = "Example"
    settings = "{}"
    verbose_logging = SzEngineFlags.SZ_NO_LOGGING
    sz_configmanager.initialize(instance_name, settings, verbose_logging)
    sz_configmanager.destroy()


def test_initialize_and_destroy_again(
    sz_configmanager: SzConfigManager,
) -> None:
    """Test SzConfigManager().initialize() and SzConfigManager.destroy()."""
    instance_name = "Example"
    settings: Dict[Any, Any] = {}
    verbose_logging = SzEngineFlags.SZ_NO_LOGGING
    sz_configmanager.initialize(instance_name, settings, verbose_logging)
    sz_configmanager.destroy()


def test_context_managment(engine_vars: Dict[Any, Any]) -> None:
    """Test the use of SzConfigGrpc in context."""
    with SzConfigManager(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    ) as sz_configmanager:
        config_id = sz_configmanager.get_default_config_id()
        actual = sz_configmanager.get_config(config_id)
        actual_json = json.loads(actual)
        assert schema(config_schema) == actual_json


# -----------------------------------------------------------------------------
# SzConfigManager fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="sz_config", scope="module")
def szconfig_fixture(engine_vars: Dict[Any, Any]) -> SzConfig:
    """
    Single engine object to use for all tests.
    engine_vars is returned from conftest.py.
    """

    result = SzConfig(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    return result


@pytest.fixture(name="sz_configmanager", scope="module")
def szconfigmanager_instance_fixture(engine_vars: Dict[Any, Any]) -> SzConfigManager:
    """Single engine object to use for all tests.
    build_engine_vars is returned from conftest.pys"""

    result = SzConfigManager(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    return result


# -----------------------------------------------------------------------------
# SzConfigManager schemas
# -----------------------------------------------------------------------------


config_list_schema = {
    "CONFIGS": [{"CONFIG_ID": int, "CONFIG_COMMENTS": str, "SYS_CREATE_DT": str}]
}

config_schema = {
    "G2_CONFIG": {
        "CFG_ATTR": [
            {
                Optional("ADVANCED"): Or(str, None),
                "ATTR_ID": int,
                "ATTR_CODE": str,
                "ATTR_CLASS": str,
                "FTYPE_CODE": Or(str, None),
                "FELEM_CODE": Or(str, None),
                "FELEM_REQ": str,
                "DEFAULT_VALUE": Or(str, None),
                "INTERNAL": Or(str, None),
            },
        ],
        "CFG_CFBOM": [
            {
                "CFCALL_ID": int,
                "FTYPE_ID": int,
                Optional("FELEM_ID"): int,
                Optional("EXEC_ORDER"): int,
            },
        ],
        "CFG_CFCALL": [
            {
                "CFCALL_ID": int,
                "FTYPE_ID": int,
                "CFUNC_ID": int,
            },
        ],
        "CFG_CFRTN": [
            {
                "CFRTN_ID": int,
                "CFUNC_ID": int,
                "FTYPE_ID": int,
                "CFUNC_RTNVAL": str,
                Optional("EXEC_ORDER"): int,
                "SAME_SCORE": int,
                "CLOSE_SCORE": int,
                "LIKELY_SCORE": int,
                "PLAUSIBLE_SCORE": int,
                "UN_LIKELY_SCORE": int,
            },
        ],
        "CFG_CFUNC": [
            {
                "CFUNC_ID": int,
                "CFUNC_CODE": str,
                "CFUNC_DESC": str,
                "CONNECT_STR": str,
                "ANON_SUPPORT": str,
                "LANGUAGE": Or(str, None),
                "JAVA_CLASS_NAME": Or(str, None),
            },
        ],
        "CFG_DFBOM": [
            {
                "DFCALL_ID": int,
                "FTYPE_ID": int,
                Optional("FELEM_ID"): int,
                Optional("EXEC_ORDER"): int,
            },
        ],
        "CFG_DFCALL": [
            {
                "DFCALL_ID": int,
                "FTYPE_ID": int,
                "DFUNC_ID": int,
            },
        ],
        "CFG_DFUNC": [
            {
                "DFUNC_ID": int,
                "DFUNC_CODE": str,
                "DFUNC_DESC": str,
                "CONNECT_STR": str,
                "ANON_SUPPORT": str,
                "LANGUAGE": Or(str, None),
                "JAVA_CLASS_NAME": Or(str, None),
            },
        ],
        "CFG_DSRC": [
            {
                "DSRC_ID": int,
                "DSRC_CODE": str,
                "DSRC_DESC": str,
                "RETENTION_LEVEL": str,
            },
        ],
        "CFG_DSRC_INTEREST": [],
        "CFG_EFBOM": [
            {
                "EFCALL_ID": int,
                "FTYPE_ID": int,
                Optional("FELEM_ID"): int,
                Optional("EXEC_ORDER"): int,
                "FELEM_REQ": str,
            },
        ],
        "CFG_EFCALL": [
            {
                "EFCALL_ID": int,
                "FTYPE_ID": int,
                Optional("FELEM_ID"): int,
                "EFUNC_ID": int,
                Optional("EXEC_ORDER"): int,
                "EFEAT_FTYPE_ID": int,
                "IS_VIRTUAL": str,
            },
        ],
        "CFG_EFUNC": [
            {
                "EFUNC_ID": int,
                "EFUNC_CODE": str,
                "EFUNC_DESC": str,
                "CONNECT_STR": str,
                "LANGUAGE": Or(str, None),
                "JAVA_CLASS_NAME": Or(str, None),
            },
        ],
        "CFG_ERFRAG": [
            {
                "ERFRAG_ID": int,
                "ERFRAG_CODE": str,
                "ERFRAG_DESC": str,
                "ERFRAG_SOURCE": str,
                "ERFRAG_DEPENDS": Or(str, None),
            },
        ],
        "CFG_ERRULE": [
            {
                "ERRULE_ID": int,
                "ERRULE_CODE": str,
                "RESOLVE": str,
                "RELATE": str,
                "RTYPE_ID": int,
                "QUAL_ERFRAG_CODE": str,
                "DISQ_ERFRAG_CODE": Or(str, None),
                "ERRULE_TIER": Or(int, None),
            },
        ],
        "CFG_FBOM": [
            {
                "FTYPE_ID": int,
                Optional("FELEM_ID"): int,
                Optional("EXEC_ORDER"): int,
                "DISPLAY_LEVEL": int,
                "DISPLAY_DELIM": Or(str, None),
                "DERIVED": str,
            },
        ],
        "CFG_FBOVR": [
            {
                "FTYPE_ID": int,
                "UTYPE_CODE": str,
                "FTYPE_FREQ": str,
                "FTYPE_EXCL": str,
                "FTYPE_STAB": str,
            },
        ],
        "CFG_FCLASS": [
            {
                "FCLASS_ID": int,
                "FCLASS_CODE": str,
                "FCLASS_DESC": str,
            },
        ],
        "CFG_FELEM": [
            {
                Optional("FELEM_ID"): int,
                "FELEM_CODE": str,
                "FELEM_DESC": str,
                "DATA_TYPE": str,
            },
        ],
        "CFG_FTYPE": [
            {
                "FTYPE_ID": int,
                "FTYPE_CODE": Or(str, None),
                "FTYPE_DESC": str,
                "FCLASS_ID": int,
                "FTYPE_FREQ": str,
                "FTYPE_EXCL": str,
                "FTYPE_STAB": str,
                "PERSIST_HISTORY": str,
                "USED_FOR_CAND": str,
                "DERIVED": str,
                "RTYPE_ID": int,
                "ANONYMIZE": str,
                "VERSION": int,
                "SHOW_IN_MATCH_KEY": str,
            },
        ],
        "CFG_GENERIC_THRESHOLD": [
            {
                "GPLAN_ID": int,
                "BEHAVIOR": str,
                "FTYPE_ID": int,
                "CANDIDATE_CAP": int,
                "SCORING_CAP": int,
                "SEND_TO_REDO": str,
            },
        ],
        "CFG_GPLAN": [
            {
                "GPLAN_ID": int,
                "GPLAN_CODE": str,
                "GPLAN_DESC": str,
            },
        ],
        "CFG_RCLASS": [
            {
                "RCLASS_ID": int,
                "RCLASS_CODE": str,
                "RCLASS_DESC": str,
                "IS_DISCLOSED": str,
            },
        ],
        "CFG_RTYPE": [
            {
                "RTYPE_ID": int,
                "RTYPE_CODE": str,
                "RTYPE_DESC": str,
                "RCLASS_ID": int,
                "BREAK_RES": str,
            },
        ],
        "CFG_SFCALL": [
            {
                "SFCALL_ID": int,
                "FTYPE_ID": int,
                Optional("FELEM_ID"): int,
                "SFUNC_ID": int,
                Optional("EXEC_ORDER"): int,
            },
        ],
        "CFG_SFUNC": [
            {
                "SFUNC_ID": int,
                "SFUNC_CODE": str,
                "SFUNC_DESC": str,
                "CONNECT_STR": str,
                "LANGUAGE": Or(str, None),
                "JAVA_CLASS_NAME": Or(str, None),
            },
        ],
        "SYS_OOM": [
            {
                "OOM_TYPE": str,
                "OOM_LEVEL": str,
                "FTYPE_ID": int,
                "THRESH1_CNT": int,
                "THRESH1_OOM": int,
                "NEXT_THRESH": int,
            },
        ],
        "CONFIG_BASE_VERSION": {
            "VERSION": str,
            "BUILD_VERSION": str,
            "BUILD_DATE": str,
            "BUILD_NUMBER": str,
            "COMPATIBILITY_VERSION": {
                "CONFIG_VERSION": str,
            },
        },
    },
}
