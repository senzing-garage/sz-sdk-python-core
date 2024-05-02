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
    sz_config = SzConfig()
    sz_config.initialize(INSTANCE_NAME, settings)

    # Do work.

    sz_config.destroy()
except SzError as err:
    print(f"\nError:\n{err}\n")
