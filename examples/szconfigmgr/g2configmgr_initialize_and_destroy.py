#! /usr/bin/env python3

from senzing import szconfigmanager
from senzing.szerror import SzError

INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_configmgr = szconfigmanager.SzConfigManager()
    sz_configmgr.initialize(INSTANCE_NAME, SETTINGS)

    # Do work.

    sz_configmgr.destroy()
except SzError as err:
    print(err)
