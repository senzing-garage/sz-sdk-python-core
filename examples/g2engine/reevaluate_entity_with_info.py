#! /usr/bin/env python3

# TODO Fix when observer is in place

from senzing import g2engine
from senzing.g2exception import G2Exception

ENTITY_ID = 1
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
    result = g2_engine.reevaluate_entity(ENTITY_ID, 1)
    print(result)
except G2Exception as err:
    print(err)
