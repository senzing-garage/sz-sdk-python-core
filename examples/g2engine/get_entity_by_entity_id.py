#! /usr/bin/env python3

from senzing import g2engine
from senzing.g2exception import G2Exception

INI_PARAMS_DICT = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
MODULE_NAME = "Example"

ENTITY_ID = 1

try:
    g2_engine = g2engine.G2Engine(MODULE_NAME, INI_PARAMS_DICT)
    result = g2_engine.get_entity_by_entity_id(ENTITY_ID)
    print(result)
except G2Exception as err:
    print(err)
