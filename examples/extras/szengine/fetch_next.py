#! /usr/bin/env python3

from senzing import SzAbstractFactory, SzAbstractFactoryParameters, SzError

FACTORY_PARAMETERS: SzAbstractFactoryParameters = {
    "instance_name": "Example",
    "settings": {
        "PIPELINE": {
            "CONFIGPATH": "/etc/opt/senzing",
            "RESOURCEPATH": "/opt/senzing/er/resources",
            "SUPPORTPATH": "/opt/senzing/data",
        },
        "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
    },
}

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
    sz_engine = sz_abstract_factory.create_sz_engine()
    export_handle = sz_engine.export_json_entity_report()
    with open("exportJSONEntityReport.json", "w", encoding="utf-8") as export_out:
        while True:
            export_record = sz_engine.fetch_next(export_handle)
            if not export_record:
                break
            export_out.write(export_record)

    sz_engine.close_export(export_handle)
except SzError as err:
    print(f"\nError in {__file__}: {err}\n")
