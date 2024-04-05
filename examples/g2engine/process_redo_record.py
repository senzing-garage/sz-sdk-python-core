#! /usr/bin/env python3

from sys import exit

from senzing import g2engine
from senzing.g2exception import G2Exception

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
    g2_engine = g2engine.G2Engine(INSTANCE_NAME, SETTINGS)
    record = g2_engine.get_redo_record()
    if not record:
        print("No redo records")
        exit(0)

    result = g2_engine.process_redo_record(record, 1)
    print(result)
except G2Exception as err:
    print(err)
