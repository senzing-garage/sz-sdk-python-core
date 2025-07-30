from senzing import (
    SzAbstractFactory,
    SzConfigManager,
    SzDiagnostic,
    SzEngine,
    SzError,
    SzProduct,
)

from senzing_core import SzAbstractFactoryCore

# Define methods using Senzing Abstract Base Classes.


def create_and_use_senzing_objects(abstract_factory: SzAbstractFactory) -> None:

    # Create Senzing objects.

    sz_configmanager = abstract_factory.create_configmanager()
    sz_diagnostic = abstract_factory.create_diagnostic()
    sz_engine = abstract_factory.create_engine()
    sz_product = abstract_factory.create_product()

    # Use Senzing objects.

    print(use_configmanager(sz_configmanager))
    print(use_diagnostic(sz_diagnostic))
    print(use_engine(sz_engine))
    print(use_product(sz_product))


def use_configmanager(configmanager: SzConfigManager) -> str:
    return configmanager.get_config_registry()


def use_diagnostic(diagnostic: SzDiagnostic) -> str:
    return diagnostic.get_repository_info()


def use_engine(engine: SzEngine) -> int:
    return engine.get_active_config_id()


def use_product(product: SzProduct) -> str:
    return product.get_version()


# Example using SzAbstractFactoryCore implementation class.

try:

    # Create an SzAbstractFactory using SzAbstractFactoryCore.

    instance_name = "Example"
    settings = {
        "PIPELINE": {
            "CONFIGPATH": "/etc/opt/senzing",
            "RESOURCEPATH": "/opt/senzing/er/resources",
            "SUPPORTPATH": "/opt/senzing/data",
        },
        "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
    }
    sz_abstract_factory = SzAbstractFactoryCore(instance_name, settings)

    # Create and use Senzing objects.

    create_and_use_senzing_objects(sz_abstract_factory)

except SzError as err:
    print(f"\nERROR: {err}\n")
