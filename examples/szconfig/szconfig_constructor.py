#! /usr/bin/env python3

from senzing import SzConfig, SzError

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
    sz_config1 = SzConfig(INSTANCE_NAME, SETTINGS)
except SzError as err:
    print(f"\nError:\n{err}\n")
