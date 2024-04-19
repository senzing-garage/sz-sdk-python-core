#! /usr/bin/env python3

from senzing import szengine
from senzing.szerror import SzError

# TODO Use a truth set entity id - in all examples
DATA_SOURCE_CODE = "TEST"
INSTANCE_NAME = "Example"
RECORD_ID = "Example-1"
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
    result = sz_engine.get_entity_by_record_id_return_dict(DATA_SOURCE_CODE, RECORD_ID)
    print(result)
except SzError as err:
    print(err)
