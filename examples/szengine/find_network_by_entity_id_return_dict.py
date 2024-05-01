#! /usr/bin/env python3

import json

from senzing import SzEngine, SzError

BUILD_OUT_DEGREE = 2
ENTITY_LIST = {"ENTITIES": [{"ENTITY_ID": 1}, {"ENTITY_ID": 4}]}
INSTANCE_NAME = "Example"
MAX_DEGREES = 5
MAX_ENTITIES = 10
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
    RESULT = sz_engine.find_network_by_entity_id_return_dict(
        ENTITY_LIST, MAX_DEGREES, BUILD_OUT_DEGREE, MAX_ENTITIES
    )
    print(json.dumps(RESULT)[:66], "...")
except SzError as err:
    print(f"\nError:\n{err}\n")
