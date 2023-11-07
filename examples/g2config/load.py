#! /usr/bin/env python3

import json
from typing import Any, Dict

from senzing import g2config
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
json_config_dict: Dict[
    str, Any
] = {}  # Naturally, this would be a full Senzing configuration.

try:
    g2_config = g2config.G2Config(MODULE_NAME, json.dumps(ini_params_dict))
    CONFIG_HANDLE = g2_config.load(json.dumps(json_config_dict))
except G2Exception as err:
    print(err)
