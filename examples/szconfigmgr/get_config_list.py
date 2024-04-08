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
    sz_configmgr = szconfigmgr.SzConfigMgr(INSTANCE_NAME, SETTINGS)
    config_list = sz_configmgr.get_config_list()
    print(config_list)
except SzException as err:
    print(err)
