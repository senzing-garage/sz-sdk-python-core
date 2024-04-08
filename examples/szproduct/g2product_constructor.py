#! /usr/bin/env python3

from szexception import SzException

from . import szproduct

INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

# Example 1

try:
    g2_product = szproduct.G2Product(INSTANCE_NAME, SETTINGS)
except SzException as err:
    print(err)

# Example 2

try:
    g2_product = szproduct.G2Product()
    g2_product.initialize(INSTANCE_NAME, SETTINGS)
except SzException as err:
    print(err)
