#! /usr/bin/env python3

from senzing import szdiagnostic
from senzing.szerror import SzError

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
    sz_diagnostic = szdiagnostic.SzDiagnostic(INSTANCE_NAME, SETTINGS)
    result = sz_diagnostic.get_data_store_info()
    print(result)
except SzError as err:
    print(err)
