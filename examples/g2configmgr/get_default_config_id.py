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
    config_id = g2_configmgr.get_default_config_id()
    print(config_id)
except SzException as err:
    print(err)
