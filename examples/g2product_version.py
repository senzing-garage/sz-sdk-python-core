#! /usr/bin/env python3

import json

from senzing import g2product
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
    G2_PRODUCT = g2product.G2Product(
        ENGINE_MODULE_NAME, json.dumps(ENGINE_CONFIGURATION)
    )
    VERSION = G2_PRODUCT.version()
    print(VERSION)
except G2Exception as err:
    print(err)
