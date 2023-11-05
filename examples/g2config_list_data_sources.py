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

try:
    G2_CONFIG = g2config.G2Config(
        ENGINE_MODULE_NAME, json.dumps(ENGINE_CONFIGURATION), 0
    )
    CONFIG_HANDLE = G2_CONFIG.create()
    RESULT = G2_CONFIG.list_data_sources(CONFIG_HANDLE)
    G2_CONFIG.close(CONFIG_HANDLE)
    print(RESULT)
except G2Exception as err:
    print(err)
