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
    sz_configmanager = SzConfigManager()
    sz_configmanager.initialize(INSTANCE_NAME, SETTINGS)

    # Do work.

    sz_configmanager.destroy()
except SzError as err:
    print(f"\nError:\n{err}\n")
