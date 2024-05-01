#! /usr/bin/env python3

from sys import exit

from senzing import SzEngineFlags, SzError, szengine

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
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    record = sz_engine.get_redo_record()
    if not record:
        print("No redo records")
        exit(0)

    RESULT = sz_engine.process_redo_record(record, SzEngineFlags.SZ_WITH_INFO)
    print(RESULT[:66], "...")
except SzError as err:
    print(f"\nError:\n{err}\n")
