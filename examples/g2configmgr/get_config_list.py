#! /usr/bin/env python3

from szexception import SzException

from . import szconfigmgr

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
    g2_configmgr = szconfigmgr.G2ConfigMgr(INSTANCE_NAME, SETTINGS)
    config_list = g2_configmgr.get_config_list()
    print(config_list)
except SzException as err:
    print(err)
