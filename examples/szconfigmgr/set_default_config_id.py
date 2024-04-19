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
    "SQL": {"CONNECTION": "sqlite3:///tmp/sqlite/G2C.db"},
}

try:
    sz_configmgr = szconfigmanager.SzConfigManager(INSTANCE_NAME, SETTINGS)

    # Getting and setting the same for demonstration purposes
    config_id = sz_configmgr.get_default_config_id()
    sz_configmgr.set_default_config_id(config_id)
except SzError as err:
    print(err)
