#! /usr/bin/env python3

from senzing import g2engine
from senzing.g2exception import G2Exception

SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@//var/opt/senzing/G2C.db"},
}
INSTANCE_NAME = "Example"

try:
    g2_engine = g2engine.G2Engine(INSTANCE_NAME, SETTINGS)
    result = g2_engine.count_redo_records()
    print(result)
except G2Exception as err:
    print(err)
