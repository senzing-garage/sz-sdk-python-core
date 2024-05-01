#! /usr/bin/env python3

import json

from senzing import SzError, szengine

INSTANCE_NAME = "Example"
END_ENTITY_ID = 4
MAX_DEGREES = 3
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
START_ENTITY_ID = 1

try:
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    RESULT = sz_engine.find_path_by_entity_id_return_dict(
        START_ENTITY_ID, END_ENTITY_ID, MAX_DEGREES
    )
    print(json.dumps(RESULT)[:66], "...")
except SzError as err:
    print(f"\nError:\n{err}\n")
