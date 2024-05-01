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
    while sz_engine.count_redo_records() > 0:
        redo_record = sz_engine.get_redo_record()
        RESULT = sz_engine.process_redo_record(redo_record, FLAGS)
        # TODO: Review this output
        print(RESULT[:66], "...")
except SzError as err:
    print(f"\nError:\n{err}\n")
