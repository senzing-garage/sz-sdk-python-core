#! /usr/bin/env python3

from senzing import szengine
from szengineflags import SzEngineFlags
from senzing.szexception import SzError

ENTITY_ID = 1
INSTANCE_NAME = "Example"
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
    result = sz_engine.reevaluate_entity(ENTITY_ID, SzEngineFlags.SZ_WITH_INFO)
    print(result)
except SzError as err:
    print(err)
