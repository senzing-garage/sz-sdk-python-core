#! /usr/bin/env python3


from senzing import g2engine
from senzing.g2exception import G2Exception

DATA_SOURCE_CODE = "TEST"
INSTANCE_NAME = "Example"
RECORD_ID = "Example-1"
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
    result = g2_engine.reevaluate_record(DATA_SOURCE_CODE, RECORD_ID, 1)
    print(result)
except G2Exception as err:
    print(err)
