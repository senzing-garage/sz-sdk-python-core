#! /usr/bin/env python3

from senzing import g2engine
from senzing.g2exception import G2Exception

BUILD_OUT_DEGREE = 2
INSTANCE_NAME = "Example"
MAX_DEGREES = 5
MAX_ENTITIES = 10
RECORD_LIST = {
    "RECORDS": [
        {"DATA_SOURCE": "REFERENCE", "RECORD_ID": "2071"},
        {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1069"},
    ]
}
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
    result = g2_engine.find_network_by_record_id(
        RECORD_LIST, MAX_DEGREES, BUILD_OUT_DEGREE, MAX_ENTITIES
    )
    print(result)
except G2Exception as err:
    print(err)
