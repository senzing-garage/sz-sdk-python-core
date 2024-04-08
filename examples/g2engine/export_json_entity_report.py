#! /usr/bin/env python3

from szexception import SzException

from . import szengine

INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}

try:
    g2_engine = szengine.G2Engine(INSTANCE_NAME, SETTINGS)
    export_handle = g2_engine.export_json_entity_report()

    with open("exportJSONEntityReport.json", "w") as export_out:
        while True:
            export_record = g2_engine.fetch_next(export_handle)
            if not export_record:
                break
            export_out.write(export_record)

    g2_engine.close_export(export_handle)

except SzException as err:
    print(err)
