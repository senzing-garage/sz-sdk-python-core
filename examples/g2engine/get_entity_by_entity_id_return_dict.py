#! /usr/bin/env python3

from szexception import SzException

from . import szengine

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
    g2_engine = szengine.G2Engine(INSTANCE_NAME, SETTINGS)
    result = g2_engine.get_entity_by_entity_id_return_dict(ENTITY_ID)
    print(result)
except SzException as err:
    print(err)
