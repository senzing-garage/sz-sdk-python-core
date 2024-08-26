#! /usr/bin/env python3

from senzing import SzEngine, SzEngineFlags, SzError

BUILD_OUT_DEGREE = 1
FLAGS = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS
INSTANCE_NAME = "Example"
MAX_DEGREES = 6
MAX_ENTITIES = 10
RECORD_KEYS = [("CUSTOMERS", "1001"), ("CUSTOMERS", "1009")]
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
    RESULT = sz_engine.find_network_by_record_id(
        RECORD_KEYS, MAX_DEGREES, BUILD_OUT_DEGREE, MAX_ENTITIES, FLAGS
    )
    print(RESULT)
except SzError as err:
    print(f"\nError: {err}\n")
