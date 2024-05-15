#! /usr/bin/env python3

import json

from senzing import SzEngine, SzError

DATA_SOURCE_CODE = "CUSTOMERS"
INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
RECORD_ID = "1001"

try:
    sz_engine = SzEngine(INSTANCE_NAME, SETTINGS)
    RESULT = sz_engine.get_record_return_dict(DATA_SOURCE_CODE, RECORD_ID)
    print(json.dumps(RESULT))
except SzError as err:
    print(f"\nError:\n{err}\n")
