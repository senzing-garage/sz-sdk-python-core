#! /usr/bin/env python3

from senzing import SzEngine, SzEngineFlags, SzError

BUILD_OUT_DEGREE = 1
ENTITY_IDS = [1, 4]
FLAGS = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS
INSTANCE_NAME = "Example"
MAX_DEGREES = 4
MAX_ENTITIES = 10
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
    RESULT = sz_engine.find_network_by_entity_id(
        ENTITY_IDS, MAX_DEGREES, BUILD_OUT_DEGREE, MAX_ENTITIES, FLAGS
    )
    print(RESULT)
except SzError as err:
    print(f"\nError: {err}\n")
