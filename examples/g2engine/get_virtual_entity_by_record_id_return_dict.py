#! /usr/bin/env python3

from senzing import g2engine
from senzing.g2exception import G2Exception

INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}
RECORD_LIST = {
    "RECORDS": [
        {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1001"},
        {"DATA_SOURCE": "CUSTOMERS", "RECORD_ID": "1022"},
    ]
}

# TODO Set sane flags or use default? Examples should show use of flags? Or examples on using flags?
try:
    g2_engine = g2engine.G2Engine(INSTANCE_NAME, SETTINGS)
    result = g2_engine.get_virtual_entity_by_record_id_return_dict(RECORD_LIST)
    print(result)
except G2Exception as err:
    print(err)
