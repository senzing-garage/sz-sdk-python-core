#! /usr/bin/env python3

import json

from senzing import g2configmgr
from senzing.g2exception import G2Exception

ini_params_dict = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
MODULE_NAME = "Example"

try:
    g2_configmgr = g2configmgr.G2ConfigMgr(MODULE_NAME, json.dumps(ini_params_dict))
    config_id = g2_configmgr.get_default_config_id()
    CONFIG_STR = g2_configmgr.get_config(config_id)
    print(CONFIG_STR)
except G2Exception as err:
    print(err)
