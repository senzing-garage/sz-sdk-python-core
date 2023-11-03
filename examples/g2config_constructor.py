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
ENGINE_VERBOSE_LOGGING = 0

# Example 1

try:
    G2_CONFIG = g2config.G2Config(ENGINE_MODULE_NAME, json.dumps(ENGINE_CONFIGURATION))
except G2Exception as err:
    print(err)

# Example 2

try:
    G2_CONFIG = g2config.G2Config()
    G2_CONFIG.init(
        ENGINE_MODULE_NAME, json.dumps(ENGINE_CONFIGURATION), ENGINE_VERBOSE_LOGGING
    )
except G2Exception as err:
    print(err)
