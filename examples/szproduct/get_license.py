#! /usr/bin/env python3

from senzing import SzError, szproduct

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
    sz_product = szproduct.SzProduct(INSTANCE_NAME, SETTINGS)
    result = sz_product.get_license()
    print(result)
except SzError as err:
    print(f"\nError:\n{err}\n")
