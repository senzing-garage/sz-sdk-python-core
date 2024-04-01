#! /usr/bin/env python3

from senzing import g2engine
from senzing.g2exception import G2Exception

INSTANCE_NAME = "Example"
END_ENTITY_ID = 137
MAX_DEGREES = 3
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}
START_ENTITY_ID = 129

try:
    g2_engine = g2engine.G2Engine(INSTANCE_NAME, SETTINGS)
    result = g2_engine.find_path_by_entity_id_return_dict(
        START_ENTITY_ID, END_ENTITY_ID, MAX_DEGREES
    )
    print(result)
except G2Exception as err:
    print(err)
