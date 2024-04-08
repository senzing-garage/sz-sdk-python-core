#! /usr/bin/env python3

from senzing import szengine
from szexception import SzException

INSTANCE_NAME = "Example"
ENTITY_ID = 1
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
    result = sz_engine.reevaluate_entity_return_dict(ENTITY_ID, 1)
    print(result)
except SzException as err:
    print(err)
