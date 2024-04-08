#! /usr/bin/env python3

from szexception import SzException

from . import szengine

END_ENTITY_ID = 200013
INSTANCE_NAME = "Example"
MAX_DEGREES = 3
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}
START_ENTITY_ID = 200003


try:
    g2_engine = szengine.G2Engine(INSTANCE_NAME, SETTINGS)
    result = g2_engine.find_path_by_entity_id(
        START_ENTITY_ID, END_ENTITY_ID, MAX_DEGREES
    )
    print(result)
except SzException as err:
    print(err)
