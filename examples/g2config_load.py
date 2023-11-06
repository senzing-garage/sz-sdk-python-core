#! /usr/bin/env python3

import json
from typing import Any, Dict

from senzing import g2config
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
JSON_CONFIG_DICT: Dict[
    str, Any
] = {}  # Naturally, this would be a full Senzing configuration.

try:
    G2_CONFIG = g2config.G2Config(MODULE_NAME, json.dumps(INI_PARAMS_DICT))
    CONFIG_HANDLE = G2_CONFIG.load(json.dumps(JSON_CONFIG_DICT))
except G2Exception as err:
    print(err)
