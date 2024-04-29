import json

import pytest
from pytest_schema import Optional, Or, schema

from senzing import SzConfigurationError, SzEngineFlags, SzError, szconfig, szerror

# -----------------------------------------------------------------------------
# SzConfig testcases
# -----------------------------------------------------------------------------


def test_exception(sz_config) -> None:
    """Test exceptions."""
    actual = sz_config.new_exception(0)
    assert isinstance(actual, Exception)


def test_constructor(engine_vars) -> None:
    """Test constructor."""
    actual = szconfig.SzConfig(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    assert isinstance(actual, szconfig.SzConfig)


def test_constructor_dict(engine_vars) -> None:
    """Test constructor."""
    actual = szconfig.SzConfig(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS_DICT"],
    )
    assert isinstance(actual, szconfig.SzConfig)


def test_constructor_bad_INSTANCE_NAME(engine_vars) -> None:
    """Test constructor."""
    bad_INSTANCE_NAME = ""
    with pytest.raises(szerror.SzError):
        actual = szconfig.SzConfig(
            bad_INSTANCE_NAME,
            engine_vars["SETTINGS"],
        )
        assert isinstance(actual, szconfig.SzConfig)


def test_constructor_bad_SETTINGS(engine_vars) -> None:
    """Test constructor."""
    bad_SETTINGS = ""
    with pytest.raises(szerror.SzError):
        actual = szconfig.SzConfig(
            engine_vars["INSTANCE_NAME"],
            bad_SETTINGS,
        )
        assert isinstance(actual, szconfig.SzConfig)


def test_add_data_source(sz_config: szconfig.SzConfig) -> None:
    """Test SzConfig().add_data_source()."""
    data_source_code = "NAME_OF_DATASOURCE"
    config_handle = sz_config.create_config()
    actual = sz_config.add_data_source(config_handle, data_source_code)
    sz_config.close_config(config_handle)
    assert isinstance(actual, str)
    actual_json = json.loads(actual)
    assert schema(add_data_source_schema) == actual_json


def test_add_data_source_dict(sz_config) -> None:
    """Test SzConfig().add_data_source()."""
    input_json_dict = {"DSRC_CODE": "NAME_OF_DATASOURCE"}
    config_handle = sz_config.create_config()
    actual = sz_config.add_data_source(config_handle, input_json_dict)
    sz_config.close_config(config_handle)
    assert isinstance(actual, str)
    actual_json = json.loads(actual)
    assert schema(add_data_source_schema) == actual_json


def test_add_data_source_bad_config_handle_type(sz_config: szconfig.SzConfig) -> None:
    """Test SzConfig().add_data_source()."""
    bad_config_handle = "string"
    data_source_code = "NAME_OF_DATASOURCE"
    with pytest.raises(TypeError):
        sz_config.add_data_source(
            bad_config_handle, data_source_code  # type: ignore[arg-type]
        )


def test_add_data_source_bad_data_source_code(
    sz_config: szconfig.SzConfig,
) -> None:
    """Test SzConfig().add_data_source()."""
    config_handle = sz_config.create_config()
    bad_data_source_code = ()  # TODO: Find a bad data sourcecode type.
    try:
        with pytest.raises(SzError):
            sz_config.add_data_source(
                config_handle, bad_data_source_code  # type: ignore[arg-type]
            )
    finally:
        sz_config.close_config(config_handle)


def test_close_config_bad_config_handle_type(sz_config: szconfig.SzConfig) -> None:
    """Test SzConfig().create()."""
    bad_config_handle = "string"
    with pytest.raises(TypeError):
        sz_config.close_config(bad_config_handle)  # type: ignore[arg-type]


def test_create_config(sz_config: szconfig.SzConfig) -> None:
    """Test SzConfig().create()."""
    config_handle = sz_config.create_config()
    assert isinstance(config_handle, int)
    assert config_handle > 0
    sz_config.close_config(config_handle)
    assert isinstance(config_handle, int)
    assert config_handle > 0


def test_delete_data_source(sz_config: szconfig.SzConfig) -> None:
    """Test SzConfig().delete_data_source()."""
    data_source_code = "TEST"
    config_handle = sz_config.create_config()
    sz_config.delete_data_source(config_handle, data_source_code)
    sz_config.close_config(config_handle)


def test_delete_data_source_bad_config_handle_type(
    sz_config: szconfig.SzConfig,
) -> None:
    """Test SzConfig().delete_data_source()."""
    data_source_code = "TEST"
    bad_config_handle = "string"
    with pytest.raises(TypeError):
        sz_config.delete_data_source(
            bad_config_handle, data_source_code  # type: ignore[arg-type]
        )


def test_delete_data_source_bad_data_source_code(
    sz_config: szconfig.SzConfig,
) -> None:
    """Test SzConfig().delete_data_source()."""
    bad_data_source_code = 0  # TODO: Find a bad data sourcecode type.
    config_handle = sz_config.create_config()
    with pytest.raises(SzError):
        sz_config.delete_data_source(
            config_handle, bad_data_source_code  # type: ignore[arg-type]
        )
    sz_config.close_config(config_handle)


def test_get_data_sources(sz_config: szconfig.SzConfig) -> None:
    """Test SzConfig().get_data_sources()."""
    config_handle = sz_config.create_config()
    actual = sz_config.get_data_sources(config_handle)
    sz_config.close_config(config_handle)
    assert isinstance(actual, str)
    actual_json = json.loads(actual)
    assert schema(get_data_sources_schema) == actual_json


def test_get_data_sources_bad_config_handle_type(
    sz_config: szconfig.SzConfig,
) -> None:
    """Test SzConfig().list_data_sources()."""
    bad_config_handle = "string"
    with pytest.raises(TypeError):
        sz_config.get_data_sources(bad_config_handle)  # type: ignore[arg-type]


def test_import_config(sz_config: szconfig.SzConfig) -> None:
    """Test SzConfig().import_config()."""
    config_handle = sz_config.create_config()
    config_definition = sz_config.export_config(config_handle)
    config_handle = sz_config.import_config(config_definition)
    assert isinstance(config_handle, int)
    assert config_handle > 0
    sz_config.close_config(config_handle)


def test_import_config_dict(sz_config: szconfig.SzConfig) -> None:
    """Test SzConfig().import_config()."""
    config_handle = sz_config.create_config()
    config_definition = sz_config.export_config(config_handle)
    config_definition_dict = json.loads(config_definition)
    config_handle = sz_config.import_config(config_definition_dict)
    assert isinstance(config_handle, int)
    assert config_handle > 0
    sz_config.close_config(config_handle)


def test_import_config_bad_config_definition_type(
    sz_config: szconfig.SzConfig,
) -> None:
    """Test SzConfig().import_config()."""
    bad_config_definition = 0
    with pytest.raises(TypeError):
        sz_config.import_config(bad_config_definition)  # type: ignore[arg-type]


def test_import_config_bad_config_definition_value(
    sz_config: szconfig.SzConfig,
) -> None:
    """Test SzConfig().import_config()."""
    bad_config_definition = '{"Just": "Junk"}'
    with pytest.raises(SzConfigurationError):
        sz_config.import_config(bad_config_definition)  # type: ignore[arg-type]


def test_export_config(sz_config: szconfig.SzConfig) -> None:
    """Test SzConfig().export_config()."""
    config_handle = sz_config.create_config()
    actual = sz_config.export_config(config_handle)
    sz_config.close_config(config_handle)
    assert isinstance(actual, str)
    actual_json = json.loads(actual)
    assert schema(export_config_schema) == actual_json


def test_export_config_bad_config_handle_type(
    sz_config: szconfig.SzConfig,
) -> None:
    """Test SzConfig().export_config()."""
    bad_config_handle = "string"
    with pytest.raises(TypeError):
        sz_config.export_config(bad_config_handle)  # type: ignore[arg-type]


def test_initialize_and_destroy(sz_config: szconfig.SzConfig) -> None:
    """Test SzConfig().initialize() and SzConfig.destroy()."""
    instance_name = "Example"
    settings = "{}"
    verbose_logging = SzEngineFlags.SZ_NO_LOGGING
    sz_config.initialize(instance_name, settings, verbose_logging)
    sz_config.destroy()


def test_initialize_and_destroy_dict(sz_config: szconfig.SzConfig) -> None:
    """Test SzConfig().init() and SzConfig.destroy()."""
    instance_name = "Example"
    settings = {}
    verbose_logging = SzEngineFlags.SZ_NO_LOGGING
    sz_config.initialize(instance_name, settings, verbose_logging)
    sz_config.destroy()


def test_initialize_and_destroy_again(sz_config: szconfig.SzConfig) -> None:
    """Test SzConfig().init() and SzConfig.destroy()."""
    instance_name = "Example"
    settings = "{}"
    verbose_logging = SzEngineFlags.SZ_NO_LOGGING
    sz_config.initialize(instance_name, settings, verbose_logging)
    sz_config.destroy()


def test_context_managment(engine_vars) -> None:
    """Test the use of SzConfigGrpc in context."""

    with szconfig.SzConfig(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    ) as sz_config:
        config_handle = sz_config.create_config()
        actual = sz_config.get_data_sources(config_handle)
        sz_config.close_config(config_handle)
        assert isinstance(actual, str)
        actual_json = json.loads(actual)
        assert schema(get_data_sources_schema) == actual_json


# -----------------------------------------------------------------------------
# SzConfig fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="sz_config", scope="module")  # type: ignore[misc]
def szconfig_fixture(engine_vars):
    """
    Single engine object to use for all tests.
    engine_vars is returned from conftest.py.
    """

    result = szconfig.SzConfig(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    return result


# -----------------------------------------------------------------------------
# SzConfig schemas
# -----------------------------------------------------------------------------

add_data_source_schema = {
    "DSRC_ID": int,
}

get_data_sources_schema = {
    "DATA_SOURCES": [
        {
            "DSRC_ID": int,
            "DSRC_CODE": str,
        },
    ]
}

export_config_schema = {
    "G2_CONFIG": {
        "CFG_ATTR": [
            {
                "ATTR_ID": int,
                "ATTR_CODE": str,
                "ATTR_CLASS": str,
                "FTYPE_CODE": Or(str, None),
                "FELEM_CODE": Or(str, None),
                "FELEM_REQ": str,
                "DEFAULT_VALUE": Or(str, None),
                Optional("ADVANCED"): Or(str, None),
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
                Optional("EXEC_ORDER"): int,
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
                Optional("FUNC_LIB"): str,
                Optional("FUNC_VER"): str,
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
                Optional("EXEC_ORDER"): int,
            },
        ],
        "CFG_DFUNC": [
            {
                "DFUNC_ID": int,
                "DFUNC_CODE": str,
                "DFUNC_DESC": str,
                Optional("FUNC_LIB"): str,
                Optional("FUNC_VER"): str,
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
                Optional("DSRC_RELY"): int,
                "RETENTION_LEVEL": str,
                Optional("CONVERSATIONAL"): str,
            },
        ],
        "CFG_DSRC_INTEREST": [],
        Optional("CFG_ECLASS"): [
            {
                Optional("ECLASS_ID"): int,
                "ECLASS_CODE": str,
                "ECLASS_DESC": str,
                "RESOLVE": str,
            },
        ],
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
                Optional("FUNC_LIB"): str,
                Optional("FUNC_VER"): str,
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
                Optional("ERRULE_DESC"): str,
                "RESOLVE": str,
                "RELATE": str,
                Optional("REF_SCORE"): int,
                "RTYPE_ID": int,
                "QUAL_ERFRAG_CODE": str,
                "DISQ_ERFRAG_CODE": Or(str, None),
                "ERRULE_TIER": Or(int, None),
            },
        ],
        Optional("CFG_ETYPE"): [
            {
                "ETYPE_ID": int,
                "ETYPE_CODE": str,
                "ETYPE_DESC": str,
                Optional("ECLASS_ID"): int,
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
                Optional("ECLASS_ID"): int,
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
                Optional("TOKENIZE"): str,
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
                Optional("DERIVATION"): Or(str, None),
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
        Optional("CFG_LENS"): [
            {
                Optional("LENS_ID"): int,
                "LENS_CODE": str,
                "LENS_DESC": str,
            },
        ],
        Optional("CFG_LENSRL"): [],
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
                Optional("REL_STRENGTH"): int,
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
                Optional("FUNC_LIB"): str,
                Optional("FUNC_VER"): str,
                "CONNECT_STR": str,
                "LANGUAGE": Or(str, None),
                "JAVA_CLASS_NAME": Or(str, None),
            },
        ],
        "SYS_OOM": [
            {
                "OOM_TYPE": str,
                "OOM_LEVEL": str,
                Optional("LENS_ID"): int,
                "FTYPE_ID": int,
                Optional("LIB_FEAT_ID"): int,
                Optional("FELEM_ID"): int,
                Optional("LIB_FELEM_ID"): int,
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
