#! /usr/bin/env python3

import json

from senzing import SzEngine, SzEngineFlags, SzError

INSTANCE_NAME = "Example"
ENTITY_ID = 1
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
    RESULT = sz_engine.reevaluate_entity_return_dict(
        ENTITY_ID, SzEngineFlags.SZ_WITH_INFO
    )
    print(json.dumps(RESULT))
except SzError as err:
    print(f"\nError:\n{err}\n")
