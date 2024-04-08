#! /usr/bin/env python3

from senzing import szconfigmgr
from szexception import SzException

CONFIG_COMMENT = "Just an example"
DATA_SOURCE_CODE = "TEST20"
INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3:///var/opt/senzing/G2C.db"},
}

try:
    sz_configmgr = szconfigmgr.SzConfigMgr(INSTANCE_NAME, SETTINGS)

    # Getting and setting the same for demonstration purposes
    config_id = sz_configmgr.get_default_config_id()
    sz_configmgr.set_default_config_id(config_id)
except SzException as err:
    print(err)
