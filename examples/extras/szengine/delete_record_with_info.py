#! /usr/bin/env python3

import json

from senzing_core import (
    SzAbstractFactory,
    SzAbstractFactoryParameters,
    SzEngineFlags,
    SzError,
)

DATA_SOURCE_CODE = "TEST"
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
RECORD_ID = "1"

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
    sz_engine = sz_abstract_factory.create_engine()
    RESULT = sz_engine.delete_record(DATA_SOURCE_CODE, RECORD_ID, SzEngineFlags.SZ_WITH_INFO)
    print(f"\n/File {__file__}:\n{json.dumps(RESULT)}\n")
except SzError as err:
    print(f"\nError in {__file__}:\n{err}\n")
