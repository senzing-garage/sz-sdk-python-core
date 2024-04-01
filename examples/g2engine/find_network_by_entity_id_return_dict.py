#! /usr/bin/env python3

from senzing import g2engine
from senzing.g2exception import G2Exception

BUILD_OUT_DEGREE = 2
ENTITY_LIST = {"ENTITIES": [{"ENTITY_ID": 96}, {"ENTITY_ID": 55}]}
INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}
MAX_DEGREES = 5
MAX_ENTITIES = 10

try:
    g2_engine = g2engine.G2Engine(INSTANCE_NAME, SETTINGS)
    result = g2_engine.find_network_by_entity_id_return_dict(
        ENTITY_LIST, MAX_DEGREES, BUILD_OUT_DEGREE, MAX_ENTITIES
    )
    print(result)
except G2Exception as err:
    print(err)
