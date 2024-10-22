#! /usr/bin/env python3

from senzing import SzEngine, SzEngineFlags, SzError

FLAGS = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS
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
    sz_engine = SzEngine(INSTANCE_NAME, SETTINGS)
    export_handle = sz_engine.export_json_entity_report(FLAGS)
    RESULT = ""
    while True:
        fragment = sz_engine.fetch_next(export_handle)
        if len(fragment) == 0:
            break
        RESULT += fragment
    sz_engine.close_export(export_handle)
    print(RESULT)
except SzError as err:
    print(f"\nError: {err}\n")
