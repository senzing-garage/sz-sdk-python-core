#! /usr/bin/env python3

from senzing import SzEngine, SzError

INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@//tmp/sqlite/G2C.db"},
}

try:
    sz_engine = SzEngine(INSTANCE_NAME, SETTINGS)
    RESULT = sz_engine.count_redo_records()
    print(RESULT)
except SzError as err:
    print(f"\nError: {err}\n")
