#! /usr/bin/env python3

from senzing import SzError

from senzing_core import SzAbstractFactoryCore

# The value of config_id is made up, this example will fail if you run it
CONFIG_ID = 2787481550
INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/er/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_abstract_factory = SzAbstractFactoryCore(INSTANCE_NAME, SETTINGS, CONFIG_ID)
except SzError as err:
    print(f"\nError: {err}\n")
