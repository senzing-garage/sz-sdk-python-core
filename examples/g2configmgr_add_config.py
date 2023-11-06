#! /usr/bin/env python3

import json
from typing import Any, Dict

from senzing import g2configmgr
from senzing.g2exception import G2Exception

INI_PARAMS_DICT = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
MODULE_NAME = "Example"
CONFIG_STR_DICT: Dict[
    str, Any
] = {}  # Naturally, this would be a full Senzing configuration.
CONFIG_COMMENTS = "Just an empty example"

try:
    G2_CONFIGMGR = g2configmgr.G2ConfigMgr(MODULE_NAME, json.dumps(INI_PARAMS_DICT))
    CONFIG_HANDLE = G2_CONFIGMGR.add_config(
        json.dumps(CONFIG_STR_DICT), CONFIG_COMMENTS
    )
except G2Exception as err:
    print(err)
