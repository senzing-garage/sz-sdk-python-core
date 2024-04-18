#! /usr/bin/env python3

from senzing import szengine
from senzing.szexception import SzError

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
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    result = sz_engine.search_by_attributes(SEARCH_DATA)
    print(result)
except SzError as err:
    print(err)
