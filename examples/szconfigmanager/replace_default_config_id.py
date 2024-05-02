#! /usr/bin/env python3

from senzing import SzConfig, SzConfigManager, SzError

CONFIG_COMMENT = "Just an example"
DATA_SOURCE_CODE = "TEST4"
INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

# TODO: Test this
try:
    sz_config = SzConfig(INSTANCE_NAME, SETTINGS)
    sz_configmanager = SzConfigManager(INSTANCE_NAME, SETTINGS)

    current_default_config_id = sz_configmanager.get_default_config_id()

    # Create a new config.

    CURRENT_CONFIG_DEFINITION = sz_configmanager.get_config(current_default_config_id)
    current_config_handle = sz_config.import_config(CURRENT_CONFIG_DEFINITION)
    sz_config.add_data_source(current_config_handle, DATA_SOURCE_CODE)
    NEW_CONFIG_DEFINITION = sz_config.export_config(current_config_handle)
    new_default_config_id = sz_configmanager.add_config(
        NEW_CONFIG_DEFINITION, CONFIG_COMMENT
    )

    # Replace default config id.

    sz_configmanager.replace_default_config_id(
        current_default_config_id, new_default_config_id
    )
except SzError as err:
    print(f"\nError:\n{err}\n")
