#! /usr/bin/env python3

from senzing import SzConfig, SzConfigManager, SzError

INSTANCE_NAME = "Example"
settings = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/er/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    # For this example, get default configuration.

    sz_configmanager = SzConfigManager(INSTANCE_NAME, settings)
    config_id = sz_configmanager.get_default_config_id()
    config_definition = sz_configmanager.get_config(config_id)

    # Import the configuration.

    sz_config = SzConfig(INSTANCE_NAME, settings)
    config_handle = sz_config.import_config(config_definition)
except SzError as err:
    print(f"\nError: {err}\n")
