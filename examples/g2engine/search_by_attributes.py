#! /usr/bin/env python3

from senzing import g2engine
from senzing.g2exception import G2Exception

INSTANCE_NAME = "Example"
SEARCH_DATA = {"NAME_FULL": "robert smith", "DATE_OF_BIRTH": "12/11/1978"}
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
    result = g2_engine.search_by_attributes(SEARCH_DATA)
    print(result)
except G2Exception as err:
    print(err)
