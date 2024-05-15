#! /usr/bin/env python3

from senzing import SzConfig, SzError

INSTANCE_NAME = "Example"
settings = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_config = SzConfig(INSTANCE_NAME, settings)
    config_handle = sz_config.create_config()  # Create first in-memory.
    CONFIG_DEFINITION = sz_config.export_config(
        config_handle
    )  # Save in-memory to string.
    sz_config.close_config(config_handle)
    print(CONFIG_DEFINITION)
except SzError as err:
    print(f"\nError:\n{err}\n")
