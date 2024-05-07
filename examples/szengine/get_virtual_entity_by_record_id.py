#! /usr/bin/env python3

from senzing import SzEngine, SzEngineFlags, SzError

FLAGS = SzEngineFlags.SZ_VIRTUAL_ENTITY_DEFAULT_FLAGS
INSTANCE_NAME = "Example"
RECORD_LIST = {
    "RECORDS": [
        {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1001"},
        {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1002"},
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
    sz_engine = SzEngine(INSTANCE_NAME, SETTINGS)
    RESULT = sz_engine.get_virtual_entity_by_record_id(RECORD_LIST, FLAGS)
    print(RESULT[:66], "...")
except SzError as err:
    print(f"\nError:\n{err}\n")
