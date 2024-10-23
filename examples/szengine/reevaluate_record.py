#! /usr/bin/env python3

from senzing import SzAbstractFactory, SzEngineFlags, SzError

DATA_SOURCE_CODE = "CUSTOMERS"
FACTORY_PARAMETERS = {
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
FLAGS = SzEngineFlags.SZ_WITH_INFO
RECORD_ID = "1001"

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
    sz_engine = sz_abstract_factory.create_sz_engine()
    RESULT = sz_engine.reevaluate_record(DATA_SOURCE_CODE, RECORD_ID, FLAGS)
    print(RESULT)
except SzError as err:
    print(f"\nError: {err}\n")
