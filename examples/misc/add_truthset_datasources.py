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
    sz_config = sz_abstract_factory.create_config()
    sz_configmanager = sz_abstract_factory.create_configmanager()
    sz_diagnostic = sz_abstract_factory.create_diagnostic()
    sz_engine = sz_abstract_factory.create_engine()

    current_default_config_id = sz_configmanager.get_default_config_id()
    OLD_CONFIG_DEFINITION = sz_configmanager.get_config(current_default_config_id)
    config_handle = sz_config.import_config(OLD_CONFIG_DEFINITION)
    for data_source_code in TRUTHSET_DATASOURCES:
        sz_config.add_data_source(config_handle, data_source_code)
    NEW_CONFIG_DEFINITION = sz_config.export_config(config_handle)
    new_default_config_id = sz_configmanager.add_config(NEW_CONFIG_DEFINITION, "Add TruthSet datasources")
    sz_configmanager.replace_default_config_id(current_default_config_id, new_default_config_id)
    sz_abstract_factory.reinitialize(new_default_config_id)
except SzError as err:
    print(f"\nERROR: {err}\n")
