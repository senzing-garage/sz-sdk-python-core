#! /usr/bin/env python3

import json

from senzing import SzError, szengine

END_DATA_SOURCE_CODE = "CUSTOMERS"
INSTANCE_NAME = "Example"
END_RECORD_ID = "1001"
MAX_DEGREES = 3
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
START_DATA_SOURCE_CODE = "CUSTOMERS"
START_RECORD_ID = "1009"

try:
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    RESULT = sz_engine.find_path_by_record_id_return_dict(
        START_DATA_SOURCE_CODE,
        START_RECORD_ID,
        END_DATA_SOURCE_CODE,
        END_RECORD_ID,
        MAX_DEGREES,
    )
    print(json.dumps(RESULT)[:66], "...")
except SzError as err:
    print(f"\nError:\n{err}\n")
