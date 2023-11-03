#! /usr/bin/env python3

import json

from senzing import g2config
from senzing.g2exception import G2Exception

ENGINE_CONFIGURATION = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
ENGINE_MODULE_NAME = "EXAMPLE"
CONFIGURATION = {}  # Naturally, this would be a full Senzing configuration.

try:
    G2_CONFIG = g2config.G2Config(
        ENGINE_MODULE_NAME, json.dumps(ENGINE_CONFIGURATION), 0
    )
    CONFIG_HANDLE_1 = G2_CONFIG.create()  # Create first in-memory.
    CONFIGURATION = G2_CONFIG.save(CONFIG_HANDLE_1)  # Save in-memory to string.
    CONFIG_HANDLE_2 = G2_CONFIG.load(CONFIGURATION)  # Create second in-memory.
    G2_CONFIG.close(CONFIG_HANDLE_1)
    G2_CONFIG.close(CONFIG_HANDLE_2)
except G2Exception as err:
    print(err)
