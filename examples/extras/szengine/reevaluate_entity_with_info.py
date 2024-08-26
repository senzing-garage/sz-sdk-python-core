#! /usr/bin/env python3

from senzing import SzEngine, SzEngineFlags, SzError

ENTITY_ID = 1
INSTANCE_NAME = "Example"
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
    RESULT = sz_engine.reevaluate_entity(ENTITY_ID, SzEngineFlags.SZ_WITH_INFO)
    print(RESULT)
except SzError as err:
    print(f"\nError: {err}\n")
