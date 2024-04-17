#! /usr/bin/env python3

from senzing import szengine
from senzing.szexception import SzException

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
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    result = sz_engine.why_records(
        DATA_SOURCE_CODE_1, RECORD_ID_1, DATA_SOURCE_CODE_2, RECORD_ID_2
    )
    print(result)
except SzException as err:
    print(err)
