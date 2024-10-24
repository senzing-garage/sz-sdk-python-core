from datetime import datetime
from typing import Any, Dict

import pytest

from senzing import (
    SzAbstractFactory,
    SzAbstractFactoryParameters,
    SzConfig,
    SzConfigManager,
    SzDiagnostic,
    SzEngine,
    SzProduct,
)

FACTORY_PARAMETERS: SzAbstractFactoryParameters = {
    "instance_name": "Example",
    "settings": {
        "PIPELINE": {
            "CONFIGPATH": "/etc/opt/senzing",
            "RESOURCEPATH": "/opt/senzing/er/resources",
            "SUPPORTPATH": "/opt/senzing/data",
        },
        "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
    },
}

# -----------------------------------------------------------------------------
# SzAbstractFactory testcases
# -----------------------------------------------------------------------------


def test_create_sz_config(sz_abstract_factory: SzAbstractFactory) -> None:
    """Create SzConfig."""
    actual = sz_abstract_factory.create_sz_config()
    assert isinstance(actual, SzConfig)


def test_create_sz_configmanager(sz_abstract_factory: SzAbstractFactory) -> None:
    """Create SzConfigManager."""
    actual = sz_abstract_factory.create_sz_configmanager()
    assert isinstance(actual, SzConfigManager)


def test_create_sz_diagnostic(sz_abstract_factory: SzAbstractFactory) -> None:
    """Create SzDiagnostic."""
    actual = sz_abstract_factory.create_sz_diagnostic()
    assert isinstance(actual, SzDiagnostic)


def test_create_sz_engine(sz_abstract_factory: SzAbstractFactory) -> None:
    """Create SzEngine."""
    actual = sz_abstract_factory.create_sz_engine()
    assert isinstance(actual, SzEngine)


def test_create_sz_product(sz_abstract_factory: SzAbstractFactory) -> None:
    """Create SzProduct."""
    actual = sz_abstract_factory.create_sz_product()
    assert isinstance(actual, SzProduct)


def test_reinitialize(sz_abstract_factory: SzAbstractFactory) -> None:
    """Create SzConfig."""

    datasources = [f"TEST_DATASOURCE_{datetime.now().timestamp()}"]

    # Create Senzing objects.

    sz_config = sz_abstract_factory.create_sz_config()
    sz_configmanager = sz_abstract_factory.create_sz_configmanager()

    # Get existing Senzing configuration.

    old_config_id = sz_configmanager.get_default_config_id()
    old_json_config = sz_configmanager.get_config(old_config_id)
    config_handle = sz_config.import_config(old_json_config)

    # Add DataSources to existing Senzing configuration.

    for datasource in datasources:
        sz_config.add_data_source(config_handle, datasource)

    # Persist new Senzing configuration.

    new_json_config = sz_config.export_config(config_handle)
    new_config_id = sz_configmanager.add_config(new_json_config, "Add My datasources")
    sz_configmanager.replace_default_config_id(old_config_id, new_config_id)

    # Update other Senzing objects.

    sz_abstract_factory.reinitialize(new_config_id)


def test_destroy(sz_abstract_factory: SzAbstractFactory) -> None:
    """Test a destroy and reinitialize."""
    sz_abstract_factory.destroy()
    sz_engine = sz_abstract_factory.create_sz_engine()
    _ = sz_engine.count_redo_records()


# -----------------------------------------------------------------------------
# SzAbstractFactory fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="sz_abstract_factory", scope="function")
def sz_abstract_factory_fixture(engine_vars: Dict[Any, Any]) -> SzAbstractFactory:
    """
    Single szconfig object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    result = SzAbstractFactory(**FACTORY_PARAMETERS)
    return result
