#! /usr/bin/env python3

import json
from typing import Any, Dict

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
config_str_dict: Dict[
    str, Any
] = {}  # Naturally, this would be a full Senzing configuration.
CONFIG_COMMENTS = "Just an empty example"

try:
    g2_configmgr = g2configmgr.G2ConfigMgr(MODULE_NAME, json.dumps(ini_params_dict))
    CONFIG_ID = g2_configmgr.add_config(json.dumps(config_str_dict), CONFIG_COMMENTS)
    g2_configmgr.set_default_config_id(CONFIG_ID)
except G2Exception as err:
    print(err)
