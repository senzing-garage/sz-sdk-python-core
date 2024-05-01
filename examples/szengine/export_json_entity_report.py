#! /usr/bin/env python3

from senzing import SzEngine, SzError

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
    export_handle = sz_engine.export_json_entity_report()

    with open("exportJSONEntityReport.json", "w") as export_out:
        while True:
            export_record = sz_engine.fetch_next(export_handle)
            if not export_record:
                break
            export_out.write(export_record)

    sz_engine.close_export(export_handle)
except SzError as err:
    print(f"\nError:\n{err}\n")
