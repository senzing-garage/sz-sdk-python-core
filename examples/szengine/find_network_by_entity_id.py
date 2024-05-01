#! /usr/bin/env python3

from senzing import SzEngineFlags, SzError, szengine

BUILD_OUT_DEGREE = 1
ENTITY_LIST = {
    "ENTITIES": [
        {"ENTITY_ID": 1},
        {"ENTITY_ID": 4},
    ]
}
FLAGS = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS
INSTANCE_NAME = "Example"
MAX_DEGREES = 2
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
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    RESULT = sz_engine.find_network_by_entity_id(
        ENTITY_LIST, MAX_DEGREES, BUILD_OUT_DEGREE, MAX_ENTITIES, FLAGS
    )
    print(RESULT[:66], "...")
except SzError as err:
    print(f"\nError:\n{err}\n")
