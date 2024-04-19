#! /usr/bin/env python3

from senzing import szengine
from senzing.szerror import SzError

INSTANCE_NAME = "Example"
RECORD_LIST = {
    "RECORDS": [
        {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1001"},
        {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1022"},
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
# TODO Set sane flags or use default? Examples should show use of flags? Or examples on using flags?
try:
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    result = sz_engine.get_virtual_entity_by_record_id(RECORD_LIST)
    print(result)
except SzError as err:
    print(err)
