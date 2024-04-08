#! /usr/bin/env python3

from szexception import SzException

from senzing import szengine

SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}
INSTANCE_NAME = "Example"

ENTITY_ID = 1

try:
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    result = sz_engine.find_interesting_entities_by_entity_id(ENTITY_ID)
    print(result)
except SzException as err:
    print(err)
