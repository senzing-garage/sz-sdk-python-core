from datetime import datetime
from typing import Any, Dict

import pytest
from senzing import (
    SzAbstractFactory,
    SzConfigManager,
    SzDiagnostic,
    SzEngine,
    SzProduct,
)

from senzing_core import SzAbstractFactoryCore

# -----------------------------------------------------------------------------
# Testcases
# -----------------------------------------------------------------------------


def test_create_configmanager(sz_abstract_factory: SzAbstractFactory) -> None:
    """Create SzConfigManager."""
    actual = sz_abstract_factory.create_configmanager()
    assert isinstance(actual, SzConfigManager)


def test_create_diagnostic(sz_abstract_factory: SzAbstractFactory) -> None:
    """Create SzDiagnostic."""
    actual = sz_abstract_factory.create_diagnostic()
    assert isinstance(actual, SzDiagnostic)


def test_create_engine(sz_abstract_factory: SzAbstractFactory) -> None:
    """Create SzEngine."""
    actual = sz_abstract_factory.create_engine()
    assert isinstance(actual, SzEngine)


def test_create_product(sz_abstract_factory: SzAbstractFactory) -> None:
    """Create SzProduct."""
    actual = sz_abstract_factory.create_product()
    assert isinstance(actual, SzProduct)


def test_reinitialize(sz_abstract_factory: SzAbstractFactory) -> None:
    """Create SzConfig."""

    datasources = [f"TEST_DATASOURCE_{datetime.now().timestamp()}"]

    # Create Senzing objects.

    sz_configmanager = sz_abstract_factory.create_configmanager()
    sz_config = sz_configmanager.create_config_from_template()

    # Add DataSources to Senzing configuration.

    for datasource in datasources:
        sz_config.add_data_source(datasource)

    # Persist new Senzing configuration.

    config_definition = sz_config.export()
    config_id = sz_configmanager.set_default_config(config_definition, "Add My datasources")

    # Update other Senzing objects.

    sz_abstract_factory.reinitialize(config_id)


# -----------------------------------------------------------------------------
# Unique testcases
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="sz_abstract_factory", scope="function")
def sz_abstract_factory_fixture(engine_vars: Dict[Any, Any]) -> SzAbstractFactory:
    """
    Single SzAbstractFactoryCore object to use for all tests.
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
