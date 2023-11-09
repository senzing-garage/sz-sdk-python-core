#! /usr/bin/env python3

import json

from senzing import g2config, g2configmgr
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
CONFIG_COMMENTS = "Just an empty example"

try:
    g2_config = g2config.G2Config(MODULE_NAME, json.dumps(ini_params_dict))
    g2_configmgr = g2configmgr.G2ConfigMgr(MODULE_NAME, json.dumps(ini_params_dict))
    config_handle = g2_config.create()
    config_str = g2_config.save(config_handle)
    CONFIG_ID = g2_configmgr.add_config(config_str, CONFIG_COMMENTS)
except G2Exception as err:
    print(err)
