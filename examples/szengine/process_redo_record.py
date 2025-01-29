#! /usr/bin/env python3

from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore

FLAGS = SzEngineFlags.SZ_WITH_INFO
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
    sz_abstract_factory = SzAbstractFactoryCore(INSTANCE_NAME, SETTINGS)
    sz_engine = sz_abstract_factory.create_engine()
    while True:
        REDO_RECORD = sz_engine.get_redo_record()
        if not REDO_RECORD:
            break
        RESULT = sz_engine.process_redo_record(REDO_RECORD, FLAGS)
        print(RESULT)
except SzError as err:
    print(f"\nERROR: {err}\n")
