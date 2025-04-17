#! /usr/bin/env python3

from senzing import SzError
from senzing_truthset import TRUTHSET_DATASOURCES

from senzing_core import SzAbstractFactoryCore

INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/er/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_abstract_factory = SzAbstractFactoryCore(INSTANCE_NAME, SETTINGS)
    sz_configmanager = sz_abstract_factory.create_configmanager()
    sz_config = sz_configmanager.create_config_from_template()

    # Create a new Senzing configuration with additional datasources.

    CURRENT_DEFAULT_CONFIG_ID = sz_configmanager.get_default_config_id()
    sz_config = sz_configmanager.create_config_from_config_id(CURRENT_DEFAULT_CONFIG_ID)
    for data_source_code in TRUTHSET_DATASOURCES:
        sz_config.add_data_source(data_source_code)

    # Persist new Senzing configuration.

    NEW_CONFIG_DEFINITION = sz_config.export()
    NEW_DEFAULT_CONFIG_ID = sz_configmanager.register_config(NEW_CONFIG_DEFINITION, "Add TruthSet datasources")

    # Make new Senzing configuration the default and the active configuration.

    sz_configmanager.replace_default_config_id(CURRENT_DEFAULT_CONFIG_ID, NEW_DEFAULT_CONFIG_ID)
    sz_abstract_factory.reinitialize(NEW_DEFAULT_CONFIG_ID)
except SzError as err:
    print(f"\nERROR: {err}\n")
