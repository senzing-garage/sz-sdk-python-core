#! /usr/bin/env python3

"""
szabstractfactory_test.py
"""


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
# Test cases
# -----------------------------------------------------------------------------


def test_create_configmanager(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.create_configmanager()."""
    actual = sz_abstractfactory.create_configmanager()
    assert isinstance(actual, SzConfigManager)


def test_create_diagnostic(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.create_diagnostic()."""
    actual = sz_abstractfactory.create_diagnostic()
    assert isinstance(actual, SzDiagnostic)


def test_create_engine(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.create_engine()."""
    actual = sz_abstractfactory.create_engine()
    assert isinstance(actual, SzEngine)


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
    datasources = [f"TEST_DATASOURCE_{datetime.now().timestamp()}"]

    # Create Senzing objects.

    sz_configmanager = sz_abstractfactory.create_configmanager()
    sz_config = sz_configmanager.create_config_from_template()

    # Add DataSources to Senzing configuration.

    for datasource in datasources:
        sz_config.register_data_source(datasource)

    # Persist new Senzing configuration.

    config_definition = sz_config.export()
    config_id = sz_configmanager.set_default_config(config_definition, "Add My datasources")

    # Update other Senzing objects.

    sz_abstractfactory.reinitialize(config_id)


# NOTE - ignore is for https://github.com/python/mypy/issues/1465
def test_property_instance_name(sz_abstractfactory: SzAbstractFactory) -> None:
    """Test SzAbstractFactory.instance_name."""
    actual = sz_abstractfactory.instance_name  # type: ignore[attr-defined]
    assert isinstance(actual, str)


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
