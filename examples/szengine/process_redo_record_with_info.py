#! /usr/bin/env python3

from sys import exit

from senzing import szengine
from szengineflags import SzEngineFlags
from senzing.szexception import SzError

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
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    record = sz_engine.get_redo_record()
    if not record:
        print("No redo records")
        exit(0)

    result = sz_engine.process_redo_record(record, SzEngineFlags.SZ_WITH_INFO)
    print(result)
except SzError as err:
    print(err)
