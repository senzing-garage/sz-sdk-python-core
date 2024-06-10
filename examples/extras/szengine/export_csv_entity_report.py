#! /usr/bin/env python3

from senzing import SzEngine, SzError

# Full list of available fields, modify to suit your preferences
# csv_headers_full = "RESOLVED_ENTITY_ID,RESOLVED_ENTITY_NAME,RELATED_ENTITY_ID,MATCH_LEVEL,MATCH_KEY,IS_DISCLOSED,IS_AMBIGUOUS,DATA_SOURCE,RECORD_ID,JSON_DATA,LAST_SEEN_DT,NAME_DATA,ATTRIBUTE_DATA,IDENTIFIER_DATA,ADDRESS_DATA,PHONE_DATA,RELATIONSHIP_DATA,ENTITY_DATA,OTHER_DATA"

# Good base for CSV headers
CSV_HEADERS = "RESOLVED_ENTITY_ID,RESOLVED_ENTITY_NAME,RELATED_ENTITY_ID,MATCH_LEVEL,MATCH_KEY,DATA_SOURCE,RECORD_ID"
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
    export_handle = sz_engine.export_csv_entity_report(CSV_HEADERS)
    with open("exportCSVEntityReport.csv", "w", encoding="utf-8") as export_out:
        while True:
            export_record = sz_engine.fetch_next(export_handle)
            if not export_record:
                break
            export_out.write(export_record)
    sz_engine.close_export(export_handle)
except SzError as err:
    print(f"\nError: {err}\n")
