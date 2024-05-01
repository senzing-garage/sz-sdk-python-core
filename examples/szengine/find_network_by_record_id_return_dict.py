#! /usr/bin/env python3

import json

from senzing import SzError, szengine

BUILD_OUT_DEGREE = 2
INSTANCE_NAME = "Example"
MAX_DEGREES = 5
MAX_ENTITIES = 10
RECORD_LIST = {
    "RECORDS": [
        {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1001"},
        {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1009"},
    ]
}
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    RESULT = sz_engine.find_network_by_record_id_return_dict(
        RECORD_LIST, MAX_DEGREES, BUILD_OUT_DEGREE, MAX_ENTITIES
    )
    print(json.dumps(RESULT)[:66], "...")
except SzError as err:
    print(f"\nError:\n{err}\n")
