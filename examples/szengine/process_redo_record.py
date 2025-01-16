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
    while 1:
        redo_record = sz_engine.get_redo_record()
        if not redo_record:
            break
        result = sz_engine.process_redo_record(redo_record, FLAGS)
        print(result)
except SzError as err:
    print(f"\nError: {err}\n")
