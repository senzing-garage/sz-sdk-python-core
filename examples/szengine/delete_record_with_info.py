#! /usr/bin/env python3

from senzing import szengine
from senzing.szerror import SzError
from szengineflags import SzEngineFlags

DATA_SOURCE_CODE = "TEST"
INSTANCE_NAME = "Example"
RECORD_ID = "Example-1"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    result = sz_engine.delete_record(
        DATA_SOURCE_CODE, RECORD_ID, SzEngineFlags.SZ_WITH_INFO
    )
    print(result)
except SzError as err:
    print(err)
