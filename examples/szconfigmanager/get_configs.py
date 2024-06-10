#! /usr/bin/env python3

from senzing import SzConfigManager, SzError

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
    sz_configmanager = SzConfigManager(INSTANCE_NAME, SETTINGS)
    CONFIG_LIST = sz_configmanager.get_configs()
    print(CONFIG_LIST)
except SzError as err:
    print(f"\nError: {err}\n")
