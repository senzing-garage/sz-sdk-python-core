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

# Example 1

try:
    sz_configmgr1 = szconfigmanager.SzConfigManager(INSTANCE_NAME, SETTINGS)
except SzError as err:
    print(f"\nError:\n{err}\n")

# Example 2

try:
    sz_configmgr2 = szconfigmanager.SzConfigManager()
    sz_configmgr2.initialize(INSTANCE_NAME, SETTINGS)
    sz_configmgr2.destroy()
except SzError as err:
    print(f"\nError:\n{err}\n")
