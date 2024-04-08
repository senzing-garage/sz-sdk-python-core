#! /usr/bin/env python3

from senzing import szconfigmgr
from szexception import SzException

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
    sz_configmgr = szconfigmgr.SzConfigMgr()
    sz_configmgr.initialize(INSTANCE_NAME, SETTINGS)

    # Do work.

    sz_configmgr.destroy()
except SzException as err:
    print(err)
