#! /usr/bin/env python3

from senzing import SzEngine, SzEngineFlags, SzError

FLAGS = SzEngineFlags.SZ_VIRTUAL_ENTITY_DEFAULT_FLAGS
INSTANCE_NAME = "Example"
RECORD_KEYS = [("CUSTOMERS", "1001"), ("CUSTOMERS", "1002")]
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
    RESULT = sz_engine.get_virtual_entity_by_record_id(RECORD_KEYS, FLAGS)
    print(RESULT)
except SzError as err:
    print(f"\nError: {err}\n")
