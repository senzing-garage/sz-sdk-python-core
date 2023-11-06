#! /usr/bin/env python3

import json

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

try:
    G2_CONFIG = g2config.G2Config(MODULE_NAME, json.dumps(INI_PARAMS_DICT))
    CONFIG_HANDLE_1 = G2_CONFIG.create()  # Create first in-memory.
    JSON_CONFIG = G2_CONFIG.save(CONFIG_HANDLE_1)  # Save in-memory to string.
    CONFIG_HANDLE_2 = G2_CONFIG.load(JSON_CONFIG)  # Create second in-memory.
    G2_CONFIG.close(CONFIG_HANDLE_1)
    G2_CONFIG.close(CONFIG_HANDLE_2)
except G2Exception as err:
    print(err)
