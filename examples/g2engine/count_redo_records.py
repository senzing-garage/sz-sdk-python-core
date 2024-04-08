#! /usr/bin/env python3

from szexception import SzException

from . import szengine

SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@//var/opt/senzing/G2C.db"},
}
INSTANCE_NAME = "Example"

try:
    g2_engine = szengine.G2Engine(INSTANCE_NAME, SETTINGS)
    result = g2_engine.count_redo_records()
    print(result)
except SzException as err:
    print(err)
