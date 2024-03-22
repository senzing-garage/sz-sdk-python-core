#! /usr/bin/env python3

from senzing import g2engine
from senzing.g2exception import G2Exception

DATA_SOURCE_CODE = "TEST"
INI_PARAMS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}
MODULE_NAME = "Example"
RECORD_ID = "Example-1"

try:
    g2_engine = g2engine.G2Engine(MODULE_NAME, INI_PARAMS)
    g2_engine.delete_record(DATA_SOURCE_CODE, RECORD_ID)
except G2Exception as err:
    print(err)
