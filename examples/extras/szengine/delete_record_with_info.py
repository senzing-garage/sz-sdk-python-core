#! /usr/bin/env python3

import json

from senzing import SzEngine, SzEngineFlags, SzError

DATA_SOURCE_CODE = "TEST"
INSTANCE_NAME = "Example"
RECORD_ID = "1"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/er/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_engine = SzEngine(INSTANCE_NAME, SETTINGS)
    RESULT = sz_engine.delete_record(
        DATA_SOURCE_CODE, RECORD_ID, SzEngineFlags.SZ_WITH_INFO
    )
    print(json.dumps(RESULT))
except SzError as err:
    print(f"\nError: {err}\n")
