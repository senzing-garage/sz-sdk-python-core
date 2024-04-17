#! /usr/bin/env python3

from senzing import szengine
from senzing.szexception import SzException

DATA_SOURCE_CODE = "TEST"
INSTANCE_NAME = "Example"
RECORD_ID = "Example-1"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}

try:
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    result = sz_engine.get_record(DATA_SOURCE_CODE, RECORD_ID)
    print(result)
except SzException as err:
    print(err)
