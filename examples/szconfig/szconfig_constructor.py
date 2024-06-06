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

# Example 1

try:
    sz_config1 = SzConfig(INSTANCE_NAME, settings)
except SzError as err:
    print(f"\nError:\n{err}\n")

# Example 2

try:
    sz_config2 = SzConfig()
    sz_config2._initialize(INSTANCE_NAME, settings)
    sz_config2.destroy()
except SzError as err:
    print(f"\nError:\n{err}\n")
