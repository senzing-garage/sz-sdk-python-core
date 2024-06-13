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

# Example 1

try:
    sz_configmanager_1 = SzConfigManager(INSTANCE_NAME, SETTINGS)
except SzError as err:
    print(f"\nError: {err}\n")

# Example 2

try:
    sz_configmanager_2 = SzConfigManager(INSTANCE_NAME, SETTINGS)
except SzError as err:
    print(f"\nError: {err}\n")
