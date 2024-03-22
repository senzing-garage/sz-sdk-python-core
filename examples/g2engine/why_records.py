#! /usr/bin/env python3

from senzing import g2engine
from senzing.g2exception import G2Exception

DATA_SOURCE_CODE_1 = "CUSTOMERS"
DATA_SOURCE_CODE_2 = "WATCHLIST"
INSTANCE_NAME = "Example"
RECORD_ID_1 = "1009"
RECORD_ID_2 = "1014"
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
    result = g2_engine.why_records(
        DATA_SOURCE_CODE_1, RECORD_ID_1, DATA_SOURCE_CODE_2, RECORD_ID_2
    )
    print(result)
except G2Exception as err:
    print(err)
