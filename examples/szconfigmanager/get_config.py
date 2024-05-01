#! /usr/bin/env python3

from senzing import SzError, szconfigmanager

INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_configmanager = szconfigmanager.SzConfigManager(INSTANCE_NAME, SETTINGS)
    config_id = sz_configmanager.get_default_config_id()
    CONFIG_DEFINITION = sz_configmanager.get_config(config_id)
    print(CONFIG_DEFINITION[:66], "...")
except SzError as err:
    print(f"\nError:\n{err}\n")
