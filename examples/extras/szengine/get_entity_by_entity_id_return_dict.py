#! /usr/bin/env python3

import json

from senzing import SzEngine, SzError

ENTITY_ID = 1
INSTANCE_NAME = "Example"
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
    RESULT = sz_engine.get_entity_by_entity_id_return_dict(ENTITY_ID)
    print(json.dumps(RESULT))
except SzError as err:
    print(f"\nError:\n{err}\n")
