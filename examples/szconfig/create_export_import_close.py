#! /usr/bin/env python3

from senzing import SzConfig, SzError

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
    sz_config = SzConfig(INSTANCE_NAME, settings)
    config_handle_1 = sz_config.create_config()  # Create first in-memory.
    CONFIG_DEFINITION = sz_config.export_config(
        config_handle_1
    )  # Save in-memory to string.
    config_handle_2 = sz_config.import_config(
        CONFIG_DEFINITION
    )  # Create second in-memory.
    sz_config.close_config(config_handle_1)
    sz_config.close_config(config_handle_2)
except SzError as err:
    print(f"\nError: {err}\n")
