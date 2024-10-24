#! /usr/bin/env python3

from senzing import (
    SzAbstractFactory,
    SzAbstractFactoryParameters,
    SzConfig,
    SzConfigManager,
    SzDiagnostic,
    SzEngine,
    SzError,
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


def test_sz_config(sz_config_local: SzConfig) -> None:
    """Just a test of parameter typing."""
    _ = sz_config_local


def test_sz_configmanager(sz_configmanager_local: SzConfigManager) -> None:
    """Just a test of parameter typing."""
    _ = sz_configmanager_local


def test_sz_diagnostic(sz_diagnostic_local: SzDiagnostic) -> None:
    """Just a test of parameter typing."""
    _ = sz_diagnostic_local


def test_sz_engine(sz_engine_local: SzEngine) -> None:
    """Just a test of parameter typing."""
    _ = sz_engine_local


def test_sz_product(sz_product_local: SzProduct) -> None:
    """Just a test of parameter typing."""
    _ = sz_product_local


try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
    sz_config = sz_abstract_factory.create_sz_config()
    sz_configmanager = sz_abstract_factory.create_sz_configmanager()
    sz_diagnostic = sz_abstract_factory.create_sz_diagnostic()
    sz_engine = sz_abstract_factory.create_sz_engine()
    sz_product = sz_abstract_factory.create_sz_product()

    test_sz_config(sz_config)
    test_sz_configmanager(sz_configmanager)
    test_sz_diagnostic(sz_diagnostic)
    test_sz_engine(sz_engine)
    test_sz_product(sz_product)

except SzError as err:
    print(f"\nError in {__file__}:\n{err}\n")
