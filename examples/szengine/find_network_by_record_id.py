#! /usr/bin/env python3

from senzing import szengine
from senzing.szerror import SzError

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
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    result = sz_engine.find_network_by_record_id(
        RECORD_LIST, MAX_DEGREES, BUILD_OUT_DEGREE, MAX_ENTITIES
    )
    print(result)
except SzError as err:
    print(err)
