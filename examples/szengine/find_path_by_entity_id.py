#! /usr/bin/env python3

from senzing import szengine
from senzing.szerror import SzError

END_ENTITY_ID = 200013
INSTANCE_NAME = "Example"
MAX_DEGREES = 3
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
START_ENTITY_ID = 200003


try:
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    result = sz_engine.find_path_by_entity_id(
        START_ENTITY_ID, END_ENTITY_ID, MAX_DEGREES
    )
    print(result)
except SzError as err:
    print(err)
