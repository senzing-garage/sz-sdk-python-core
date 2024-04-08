#! /usr/bin/env python3

from senzing import szproduct
from szexception import SzException

INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_product = szproduct.SzProduct()
    sz_product.initialize(INSTANCE_NAME, SETTINGS)

    # Do work.

    sz_product.destroy()
except SzException as err:
    print(err)
