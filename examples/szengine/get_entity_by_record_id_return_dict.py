#! /usr/bin/env python3

import json

from senzing import SzEngine, SzError

DATA_SOURCE_CODE = "CUSTOMERS"
INSTANCE_NAME = "Example"
RECORD_ID = "1001"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_engine = SzEngine(INSTANCE_NAME, SETTINGS)
    RESULT = sz_engine.get_entity_by_record_id_return_dict(DATA_SOURCE_CODE, RECORD_ID)
    print(json.dumps(RESULT)[:66], "...")
except SzError as err:
    print(f"\nError:\n{err}\n")
