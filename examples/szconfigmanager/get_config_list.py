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
    CONFIG_LIST = sz_configmanager.get_config_list()
    print(CONFIG_LIST[:66], "...")
except SzError as err:
    print(f"\nError:\n{err}\n")
