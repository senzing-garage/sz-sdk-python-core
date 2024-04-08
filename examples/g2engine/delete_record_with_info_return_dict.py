#! /usr/bin/env python3

from szexception import SzException

from . import szengine

DATA_SOURCE_CODE = "TEST"
INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}
RECORD_ID = "Example-1"

try:
    g2_engine = szengine.G2Engine(INSTANCE_NAME, SETTINGS)
    result = g2_engine.delete_record_return_dict(DATA_SOURCE_CODE, RECORD_ID, 1)
    print(result)
except SzException as err:
    print(err)
