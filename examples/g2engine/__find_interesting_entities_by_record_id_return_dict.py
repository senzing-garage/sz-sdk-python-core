#! /usr/bin/env python3

from senzing import g2engine
from senzing.g2exception import G2Exception

SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}
INSTANCE_NAME = "Example"

# TODO Use a truth set entity id - in all examples
DATA_SOURCE_CODE = "TEST"
RECORD_ID = "Example-1"

try:
    g2_engine = g2engine.G2Engine(INSTANCE_NAME, SETTINGS)
    result = g2_engine.find_interesting_entities_by_record_id_return_dict(
        DATA_SOURCE_CODE, RECORD_ID = {
    )
    print(result)
except G2Exception as err:
    print(err)
