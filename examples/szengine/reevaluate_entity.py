#! /usr/bin/env python3

from senzing import szengine
from senzing.szerror import SzError

ENTITY_ID = 1
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
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    sz_engine.reevaluate_entity(ENTITY_ID)
except SzError as err:
    print(err)
