#! /usr/bin/env python3

from senzing import SzEngine, SzEngineFlags, SzError

FLAGS = SzEngineFlags.SZ_WITH_INFO
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
    while True:
        redo_record = sz_engine.get_redo_record()
        if not redo_record:
            break
        RESULT = sz_engine.process_redo_record(redo_record, FLAGS)
        print(RESULT)
except SzError as err:
    print(f"\nError: {err}\n")
