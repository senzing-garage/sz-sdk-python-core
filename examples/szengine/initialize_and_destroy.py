#! /usr/bin/env python3

from senzing import szengine
from senzing.szexception import SzException

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
    sz_engine = szengine.SzEngine()
    sz_engine.initialize(INSTANCE_NAME, SETTINGS)
    # Do Work
    sz_engine.destroy()
except SzException as err:
    print(err)
