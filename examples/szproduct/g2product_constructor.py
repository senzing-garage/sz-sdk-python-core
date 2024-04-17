#! /usr/bin/env python3

from senzing import szproduct
from senzing.szexception import SzException

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
    sz_product1 = szproduct.SzProduct(INSTANCE_NAME, SETTINGS)
except SzException as err:
    print(err)

# Example 2

try:
    sz_product2 = szproduct.SzProduct()
    sz_product2.initialize(INSTANCE_NAME, SETTINGS)
    sz_product2.destroy()
except SzException as err:
    print(err)
