#! /usr/bin/env python3

import json

from senzing import g2product
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

# Example 1

try:
    g2_product = g2product.G2Product(MODULE_NAME, json.dumps(ini_params_dict))
except G2Exception as err:
    print(err)

# Example 2

try:
    g2_product = g2product.G2Product()
    g2_product.init(MODULE_NAME, json.dumps(ini_params_dict))
except G2Exception as err:
    print(err)
