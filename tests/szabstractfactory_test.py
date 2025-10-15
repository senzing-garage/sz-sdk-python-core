#! /usr/bin/env python3

"""
szabstractfactory_test.py
"""


from typing import Any, Dict

import pytest
from senzing import (
    SzAbstractFactory,
    SzConfigManager,
    SzDiagnostic,
    SzEngine,
    SzProduct,
    SzSdkError,
)

from senzing_core import (
    SzAbstractFactoryCore,
    SzConfigManagerCore,
    SzDiagnosticCore,
    SzEngineCore,
    SzProductCore,
)

# pylint: disable=protected-access

# -----------------------------------------------------------------------------
# Test cases
# -----------------------------------------------------------------------------


def test_create_same_settings(engine_vars: Dict[Any, Any]) -> None:
    """Test SzAbstractFactoryCore with the same settings."""
    factory_parameters = {"instance_name": "Example", "settings": engine_vars.get("SETTINGS_DICT", {})}
    factory_1 = SzAbstractFactoryCore(**factory_parameters)
    factory_2 = SzAbstractFactoryCore(**factory_parameters)
    assert factory_1 is factory_2


# def test_create_with_different_settings(engine_vars: Dict[Any, Any]) -> None:
#     """Test SzAbstractFactoryCore with different settings."""
#     factory_parameters_1 = {"instance_name": "Example_1", "settings": engine_vars.get("SETTINGS_DICT", {})}
#     factory_parameters_2 = {"instance_name": "Example_2", "settings": engine_vars.get("SETTINGS_DICT", {})}
#     factory = SzAbstractFactoryCore(**factory_parameters_1)  # pylint: disable=unused-variable # noqa: F841
#     with pytest.raises(SzSdkError):
#         SzAbstractFactoryCore(**factory_parameters_2)


def test_create_engine(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.create_engine()."""
    actual = sz_abstractfactory.create_engine()
    assert isinstance(actual, SzEngine)


def test_create_configmanager(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.create_configmanager()."""
    actual = sz_abstractfactory.create_configmanager()
    assert isinstance(actual, SzConfigManager)


def test_create_diagnostic(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.create_diagnostic()."""
    actual = sz_abstractfactory.create_diagnostic()
    assert isinstance(actual, SzDiagnostic)


def test_create_product(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.create_product()."""
    actual = sz_abstractfactory.create_product()
    assert isinstance(actual, SzProduct)


def test_help_1(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.help()."""
    sz_abstractfactory.help()


def test_help_2(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.help(...)."""
    sz_abstractfactory.help("create_configmanager")


def test_reinitialize(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.reinitialize()."""
    datasource = "TEST_FACTORY_REINIT"

    # Create Senzing objects.
    sz_diagnostic = sz_abstractfactory.create_diagnostic()
    sz_engine = sz_abstractfactory.create_engine()
    sz_configmanager = sz_abstractfactory.create_configmanager()
    current_config_id = sz_configmanager.get_default_config_id()
    sz_config = sz_configmanager.create_config_from_config_id(current_config_id)

    # Use engines
    _ = sz_diagnostic.get_repository_info()
    _ = sz_engine.add_record("TEST", "787B", '{"NAME_FULL":"Testy McTester"}')
    active_id_1 = sz_engine.get_active_config_id()

    # Add DataSources to Senzing configuration.
    sz_config.register_data_source(datasource)

    # Persist new Senzing configuration.
    config_definition = sz_config.export()
    new_config_id = sz_configmanager.register_config(config_definition, "Test")
    sz_configmanager.replace_default_config_id(current_config_id, new_config_id)

    # Update other Senzing objects.
    sz_abstractfactory.reinitialize(new_config_id)

    # # Use engines
    _ = sz_diagnostic.get_repository_info()
    _ = sz_engine.add_record(datasource, "767B", '{"NAME_FULL":"McTester Testy"}')
    active_id_2 = sz_engine.get_active_config_id()

    assert active_id_1 != active_id_2


# NOTE - ignore is for https://github.com/python/mypy/issues/1465
def test_property_instance_name(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.instance_name."""
    actual = sz_abstractfactory.instance_name  # type: ignore[attr-defined]
    assert isinstance(actual, str)


def test_property_is_destroyed(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.is_destroyed."""
    actual = sz_abstractfactory.is_destroyed  # type: ignore[attr-defined]
    assert isinstance(actual, bool)


def test_property_settings(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.settings."""
    actual = sz_abstractfactory.settings  # type: ignore[attr-defined]
    assert isinstance(actual, (str, dict))


def test_property_config_id(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.config_id."""
    actual = sz_abstractfactory.config_id  # type: ignore[attr-defined]
    assert isinstance(actual, int)


def test_property_verbose_logging(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.verbose_logging."""
    actual = sz_abstractfactory.verbose_logging  # type: ignore[attr-defined]
    assert isinstance(actual, int)


def test_delete_factory(engine_vars: Dict[Any, Any]) -> None:
    """Test delete on SzAbstractFactory doesn't allow use"""
    factory_parameters = {"instance_name": "Example_1", "settings": engine_vars.get("SETTINGS_DICT", {})}
    sz_factory = SzAbstractFactoryCore(**factory_parameters)
    sz_configmanager = sz_factory.create_configmanager()
    sz_diagnostic = sz_factory.create_diagnostic()
    sz_engine = sz_factory.create_engine()
    sz_product = sz_factory.create_product()
    del sz_factory

    with pytest.raises(SzSdkError):
        sz_configmanager.get_default_config_id()

    with pytest.raises(SzSdkError):
        sz_diagnostic.get_repository_info()

    with pytest.raises(SzSdkError):
        sz_engine.get_active_config_id()

    with pytest.raises(SzSdkError):
        sz_product.get_version()


def test_is_destroyed(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test destroying SzAbstractFactory also marks factory as destroyed"""
    sz_abstractfactory.destroy()
    assert sz_abstractfactory._is_destroyed  # type: ignore [attr-defined]


def test_destroy_empty_weakref_dicts(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test destroying SzAbstractFactory resets class variables for weak references"""
    sz_abstractfactory.destroy()
    assert len(SzAbstractFactoryCore._engine_instances) == 0
    assert len(SzAbstractFactoryCore._factory_instances) == 0


def test_destroy_method_calls(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test destroying SzAbstractFactory doesn't allow method use"""
    sz_abstractfactory.destroy()
    with pytest.raises(SzSdkError):
        sz_abstractfactory.create_engine()


def test_destroy_create_new_factory(engine_vars: Dict[Any, Any]) -> None:
    """Test destroying SzAbstractFactory allows a new factory"""
    factory_parameters = {"instance_name": "Example_1", "settings": engine_vars.get("SETTINGS_DICT", {})}
    factory_1 = SzAbstractFactoryCore(**factory_parameters)
    factory_1.destroy()
    factory_2 = SzAbstractFactoryCore(**factory_parameters)
    assert not factory_2.is_destroyed


def test_destroy_create_new_factory_different_arguments(engine_vars: Dict[Any, Any]) -> None:
    """Test destroying SzAbstractFactory allows a new factory with different arguments"""
    factory_parameters_1 = {"instance_name": "Example_1", "settings": engine_vars.get("SETTINGS_DICT", {})}
    factory_parameters_2 = {"instance_name": "Example_2", "settings": engine_vars.get("SETTINGS_DICT", {})}
    factory_1 = SzAbstractFactoryCore(**factory_parameters_1)
    factory_1.destroy()
    factory_2 = SzAbstractFactoryCore(**factory_parameters_2)
    assert not factory_2.is_destroyed


def test_destroy_create_new_factory_with_work(engine_vars: Dict[Any, Any]) -> None:
    """Test destroying SzAbstractFactory allows a new factory with work"""
    factory_parameters_1 = {"instance_name": "Example_1", "settings": engine_vars.get("SETTINGS_DICT", {})}
    factory_parameters_2 = {"instance_name": "Example_2", "settings": engine_vars.get("SETTINGS_DICT", {})}
    factory_1 = SzAbstractFactoryCore(**factory_parameters_1)
    sz_engine_1 = factory_1.create_engine()
    _ = sz_engine_1.add_record("TEST", "TEST787B", '{"NAME_FULL": "Mr Test McTesting"}')
    factory_1.destroy()

    factory_2 = SzAbstractFactoryCore(**factory_parameters_2)
    sz_engine_2 = factory_2.create_engine()
    _ = sz_engine_2.add_record("TEST", "TEST767B", '{"NAME_FULL": "Mr McTesting TEST"}')

    assert factory_1.is_destroyed
    assert factory_1 != factory_2


def test_destroy_szconfigmanager_is_destroyed(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test destroying SzAbstractFactory doesn't allow use of szconfigmanager"""
    sz_configmanager = sz_abstractfactory.create_configmanager()
    _ = sz_configmanager.get_default_config_id()
    sz_abstractfactory.destroy()
    with pytest.raises(SzSdkError):
        sz_configmanager.get_default_config_id()


def test_destroy_szdiagnostic_is_destroyed(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test destroying SzAbstractFactory doesn't allow use of szdiagnostic"""
    sz_diagnostic = sz_abstractfactory.create_diagnostic()
    _ = sz_diagnostic.get_repository_info()
    sz_abstractfactory.destroy()
    with pytest.raises(SzSdkError):
        sz_diagnostic.get_repository_info()


def test_destroy_szengine_is_destroyed(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test destroying SzAbstractFactory doesn't allow use of szengine"""
    sz_engine = sz_abstractfactory.create_engine()
    _ = sz_engine.get_active_config_id()
    sz_abstractfactory.destroy()
    with pytest.raises(SzSdkError):
        sz_engine.get_active_config_id()


def test_destroy_szproduct_is_destroyed(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test destroying SzAbstractFactory doesn't allow use of szproduct"""
    sz_product = sz_abstractfactory.create_product()
    _ = sz_product.get_version()
    sz_abstractfactory.destroy()
    with pytest.raises(SzSdkError):
        sz_product.get_version()


def test_destroy_all_engines_are_destroyed(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test destroying SzAbstractFactory doesn't allow use of any engines"""
    sz_configmanager = sz_abstractfactory.create_configmanager()
    sz_diagnostic = sz_abstractfactory.create_diagnostic()
    sz_engine = sz_abstractfactory.create_engine()
    sz_product = sz_abstractfactory.create_product()
    sz_abstractfactory.destroy()

    with pytest.raises(SzSdkError):
        sz_configmanager.get_default_config_id()

    with pytest.raises(SzSdkError):
        sz_diagnostic.get_repository_info()

    with pytest.raises(SzSdkError):
        sz_engine.get_active_config_id()

    with pytest.raises(SzSdkError):
        sz_product.get_version()


def test_destroy_all_engines_are_destroyed_multiple(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test destroying SzAbstractFactory doesn't allow use of szproduct"""
    sz_configmanager_1 = sz_abstractfactory.create_configmanager()
    sz_configmanager_2 = sz_abstractfactory.create_configmanager()
    sz_diagnostic_1 = sz_abstractfactory.create_diagnostic()
    sz_diagnostic_2 = sz_abstractfactory.create_diagnostic()
    sz_engine_1 = sz_abstractfactory.create_engine()
    sz_engine_2 = sz_abstractfactory.create_engine()
    sz_product_1 = sz_abstractfactory.create_product()
    sz_product_2 = sz_abstractfactory.create_product()
    sz_abstractfactory.destroy()

    with pytest.raises(SzSdkError):
        sz_configmanager_1.get_default_config_id()

    with pytest.raises(SzSdkError):
        sz_configmanager_2.get_default_config_id()

    with pytest.raises(SzSdkError):
        sz_diagnostic_1.get_repository_info()

    with pytest.raises(SzSdkError):
        sz_diagnostic_2.get_repository_info()

    with pytest.raises(SzSdkError):
        sz_engine_1.get_active_config_id()

    with pytest.raises(SzSdkError):
        sz_engine_2.get_active_config_id()

    with pytest.raises(SzSdkError):
        sz_product_1.get_version()

    with pytest.raises(SzSdkError):
        sz_product_2.get_version()


def test_create_args_hash(engine_vars: Dict[Any, Any]) -> None:
    """Test SzAbstractFactory _create_args_hash"""
    factory_parameters = {
        "instance_name": "Example",
        "settings": engine_vars.get("SETTINGS_DICT", {}),
        "config_id": 0,
        "verbose_logging": 0,
    }
    sz_factory = SzAbstractFactoryCore(**factory_parameters)
    actual = sz_factory._create_args_hash(
        factory_parameters["instance_name"],
        factory_parameters["settings"],
        factory_parameters["config_id"],
        factory_parameters["verbose_logging"],
    )
    assert isinstance(actual, str)


def test_create_args_hash_remove_whitespace() -> None:
    """Test SzAbstractFactory _create_args_hash removing whitespace"""
    factory_parameters_1 = {
        "instance_name": "Example",
        "settings": '{"PIPELINE":{"CONFIGPATH":"/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/er/resources","SUPPORTPATH":"/opt/senzing/data"},"SQL":{"CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db"}}',
        "config_id": 0,
        "verbose_logging": 0,
    }
    factory_parameters_2 = {
        "instance_name": "     Example  ",
        "settings": '    {"PIPELINE": {"CONFIGPATH": "/etc/opt/senzing", "RESOURCEPATH": "/opt/senzing/er/resources", "SUPPORTPATH": "/opt/senzing/data"}, "SQL"   :    {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"}}   ',
        "config_id": 0,
        "verbose_logging": 0,
    }
    sz_factory = SzAbstractFactoryCore(**factory_parameters_1)  # type: ignore
    factory_1 = sz_factory._create_args_hash(
        factory_parameters_1["instance_name"],  # type: ignore
        factory_parameters_1["settings"],  # type: ignore
        factory_parameters_1["config_id"],  # type: ignore
        factory_parameters_1["verbose_logging"],  # type: ignore
    )
    factory_2 = sz_factory._create_args_hash(
        factory_parameters_2["instance_name"],  # type: ignore
        factory_parameters_2["settings"],  # type: ignore
        factory_parameters_2["config_id"],  # type: ignore
        factory_parameters_2["verbose_logging"],  # type: ignore
    )
    assert factory_1 == factory_2


def test_create_args_hash_bad_type(engine_vars: Dict[Any, Any]) -> None:
    """Test SzAbstractFactory _create_args_hash with a bad type"""
    factory_parameters = {
        "instance_name": "Example",
        "settings": engine_vars.get("SETTINGS_DICT", {}),
        "config_id": 0,
        "verbose_logging": ["bad", "type"],
    }
    with pytest.raises(SzSdkError):
        SzAbstractFactoryCore(**factory_parameters)


def test_create_args_hash_different_ordered_strings() -> None:
    """Test SzAbstractFactory _create_args_hash ordering"""
    instance_name_1 = "Example"
    settings_1 = '{"PIPELINE":{"CONFIGPATH":"/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/er/resources","SUPPORTPATH":"/opt/senzing/data"},"SQL":{"CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db"}}'
    config_id_1 = 0
    verbose_logging_1 = 0
    instance_name_2 = "Example"
    settings_2 = '{"SQL":{"CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db"},"PIPELINE":{"CONFIGPATH":"/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/er/resources","SUPPORTPATH":"/opt/senzing/data"}}'
    config_id_2 = 0
    verbose_logging_2 = 0

    hash_1 = SzAbstractFactoryCore._create_args_hash(instance_name_1, settings_1, config_id_1, verbose_logging_1)
    hash_2 = SzAbstractFactoryCore._create_args_hash(instance_name_2, settings_2, config_id_2, verbose_logging_2)
    assert hash_1 == hash_2


def test_create_args_hash_different_ordered_strings_whitespace() -> None:
    """Test SzAbstractFactory _create_args_hash ordering"""
    instance_name_1 = "Example"
    settings_1 = '{"PIPELINE":{"CONFIGPATH":"/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/er/resources","SUPPORTPATH":"/opt/senzing/data"},"SQL":{"CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db"}}'
    config_id_1 = 0
    verbose_logging_1 = 0
    instance_name_2 = "   Example      "
    settings_2 = '{"SQL   ":{"   CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db  "},"PIPELINE":{"CONFIGPATH":  "/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/er/resources","SUPPORTPATH":"/opt/senzing/data"  } }   '
    config_id_2 = 0
    verbose_logging_2 = 0

    hash_1 = SzAbstractFactoryCore._create_args_hash(instance_name_1, settings_1, config_id_1, verbose_logging_1)
    hash_2 = SzAbstractFactoryCore._create_args_hash(instance_name_2, settings_2, config_id_2, verbose_logging_2)
    assert hash_1 == hash_2


def test_create_args_hash_different_ordered_dicts() -> None:
    """Test SzAbstractFactory _create_args_hash ordering"""
    factory_parameters_1 = {
        "instance_name": "Example",
        "settings": {
            "PIPELINE": {
                "CONFIGPATH": "/etc/opt/senzing",
                "RESOURCEPATH": "/opt/senzing/er/resources",
                "SUPPORTPATH": "/opt/senzing/data",
            },
            "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
        },
        "config_id": 0,
        "verbose_logging": 0,
    }
    factory_parameters_2 = {
        "instance_name": "Example",
        "settings": {
            "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
            "PIPELINE": {
                "SUPPORTPATH": "/opt/senzing/data",
                "CONFIGPATH": "/etc/opt/senzing",
                "RESOURCEPATH": "/opt/senzing/er/resources",
            },
        },
        "config_id": 0,
        "verbose_logging": 0,
    }

    hash_1 = SzAbstractFactoryCore._create_args_hash(
        factory_parameters_1["instance_name"],  # type: ignore
        factory_parameters_1["settings"],  # type: ignore
        factory_parameters_1["config_id"],  # type: ignore
        factory_parameters_1["verbose_logging"],  # type: ignore
    )
    hash_2 = SzAbstractFactoryCore._create_args_hash(
        factory_parameters_2["instance_name"],  # type: ignore
        factory_parameters_2["settings"],  # type: ignore
        factory_parameters_2["config_id"],  # type: ignore
        factory_parameters_2["verbose_logging"],  # type: ignore
    )
    assert hash_1 == hash_2


def test_create_args_hash_different_ordered_strings_and_dict() -> None:
    """Test SzAbstractFactory _create_args_hash ordering"""
    instance_name = "Example"
    settings = '{"SQL   ":{"   CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db  "},"PIPELINE":{"CONFIGPATH":  "/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/er/resources","SUPPORTPATH":"/opt/senzing/data"  } }   '
    config_id = 0
    verbose_logging = 0

    factory_parameters = {
        "instance_name": "Example",
        "settings": {
            "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
            "PIPELINE": {
                "SUPPORTPATH": "/opt/senzing/data",
                "CONFIGPATH": "/etc/opt/senzing",
                "RESOURCEPATH": "/opt/senzing/er/resources",
            },
        },
        "config_id": 0,
        "verbose_logging": 0,
    }

    hash_1 = SzAbstractFactoryCore._create_args_hash(instance_name, settings, config_id, verbose_logging)
    hash_2 = SzAbstractFactoryCore._create_args_hash(
        factory_parameters["instance_name"],  # type: ignore
        factory_parameters["settings"],  # type: ignore
        factory_parameters["config_id"],  # type: ignore
        factory_parameters["verbose_logging"],  # type: ignore
    )
    assert hash_1 == hash_2


def test_is_destroyed_szconfigmanager_all_methods(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test destroying SzAbstractFactory doesn't allow use of any methods"""
    methods = [
        m
        for m in dir(SzConfigManagerCore)
        if callable(getattr(SzConfigManagerCore, m))
        and not (m.startswith("__") or m in ("_destroy", "help", "_internal_only_destroy"))
    ]
    sz_configmanager = sz_abstractfactory.create_configmanager()
    sz_configmanager._is_destroyed = True  # type: ignore

    for method in methods:
        with pytest.raises(SzSdkError):
            getattr(SzConfigManagerCore, method)(sz_configmanager)


def test_is_destroyed_szdiagnostic_all_methods(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test destroying SzAbstractFactory doesn't allow use of any methods"""
    methods = [
        m
        for m in dir(SzDiagnosticCore)
        if callable(getattr(SzDiagnosticCore, m))
        and not (m.startswith("__") or m in ("_destroy", "help", "_internal_only_destroy"))
    ]
    sz_diagnostic = sz_abstractfactory.create_diagnostic()
    sz_diagnostic._is_destroyed = True  # type: ignore

    for method in methods:
        with pytest.raises(SzSdkError):
            getattr(SzDiagnosticCore, method)(sz_diagnostic)


def test_is_destroyed_szengine_all_methods(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test destroying SzAbstractFactory doesn't allow use of any methods"""
    methods = [
        m
        for m in dir(SzEngineCore)
        if callable(getattr(SzEngineCore, m))
        and not (m.startswith("__") or m in ("_destroy", "help", "_internal_only_destroy"))
    ]
    sz_engine = sz_abstractfactory.create_engine()
    sz_engine._is_destroyed = True  # type: ignore

    for method in methods:
        with pytest.raises(SzSdkError):
            getattr(SzEngineCore, method)(sz_engine)


def test_is_destroyed_szproduct_all_methods(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test destroying SzAbstractFactory doesn't allow use of any methods"""
    methods = [
        m
        for m in dir(SzProductCore)
        if callable(getattr(SzProductCore, m))
        and not (m.startswith("__") or m in ("_destroy", "help", "_internal_only_destroy"))
    ]
    sz_product = sz_abstractfactory.create_product()
    sz_product._is_destroyed = True  # type: ignore

    for method in methods:
        with pytest.raises(SzSdkError):
            getattr(SzProductCore, method)(sz_product)


def test_is_destroyed_factory_all_methods(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test destroying SzAbstractFactory doesn't allow use of any methods"""
    methods = [
        m
        for m in dir(SzAbstractFactoryCore)
        if callable(getattr(SzAbstractFactoryCore, m))
        and not (m.startswith("__") or m in ("_destroy", "help", "_create_args_hash", "_do_destroy"))
    ]
    sz_abstractfactory.destroy()

    for method in methods:
        with pytest.raises(SzSdkError):
            getattr(SzAbstractFactoryCore, method)(sz_abstractfactory)


def test_method_chain(engine_vars: Dict[Any, Any]) -> None:
    """Test SzAbstractFactory engine destruction on method chain"""

    factory_parameters = {
        "instance_name": "Example",
        "settings": engine_vars.get("SETTINGS_DICT", {}),
        "config_id": 0,
        "verbose_logging": 0,
    }

    sz_engine = SzAbstractFactoryCore(**factory_parameters).create_engine()
    with pytest.raises(SzSdkError):
        sz_engine.get_active_config_id()


# def test_context_manager(engine_vars: Dict[Any, Any]) -> None:
#     """Test SzAbstractFactory context manager"""

#     factory_parameters = {
#         "instance_name": "Example",
#         "settings": engine_vars.get("SETTINGS_DICT", {}),
#         "config_id": 0,
#         "verbose_logging": 0,
#     }

#     # fmt: off
#     # pylint: disable=not-context-manager
#     with pytest.raises(AttributeError, TypeError):  # type: ignore
#         with SzAbstractFactoryCore(**factory_parameters) as sz_factory:  # type: ignore
#             sz_factory.create_engine()
#     # pylint: enable=not-context-manager
#     # fmt: on


# -----------------------------------------------------------------------------
# Unique testcases
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="sz_abstractfactory", scope="function")
def szabstractfactory_fixture(engine_vars: Dict[Any, Any]) -> SzAbstractFactory:
    """
    SzAbstractFactory object to use for all tests.
    """

    factory_parameters = {
        "instance_name": "Example",
        "settings": engine_vars.get("SETTINGS_DICT", {}),
    }
    result = SzAbstractFactoryCore(**factory_parameters)
    return result


# -----------------------------------------------------------------------------
# Schemas
# -----------------------------------------------------------------------------
