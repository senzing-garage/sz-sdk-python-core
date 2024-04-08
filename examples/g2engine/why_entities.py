#! /usr/bin/env python3

from szexception import SzException

from . import szengine

ENTITY_ID_1 = 1
ENTITY_ID_2 = 6
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
    g2_engine = szengine.G2Engine(INSTANCE_NAME, SETTINGS)
    result = g2_engine.why_entities(ENTITY_ID_1, ENTITY_ID_2)
    print(result)
except SzException as err:
    print(err)
