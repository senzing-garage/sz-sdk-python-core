#! /usr/bin/env python3

import json

from senzing import SzEngine, SzError

DATA_SOURCE_CODE_1 = "CUSTOMERS"
DATA_SOURCE_CODE_2 = "CUSTOMERS"
INSTANCE_NAME = "Example"
RECORD_ID_1 = "1001"
RECORD_ID_2 = "1009"
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
    RESULT = sz_engine.why_records_return_dict(
        DATA_SOURCE_CODE_1, RECORD_ID_1, DATA_SOURCE_CODE_2, RECORD_ID_2, 1
    )
    print(json.dumps(RESULT)[:66], "...")
except SzError as err:
    print(f"\nError:\n{err}\n")
