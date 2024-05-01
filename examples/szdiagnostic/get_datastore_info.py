#! /usr/bin/env python3

from senzing import SzError, szdiagnostic

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
    RESULT = sz_diagnostic.get_datastore_info()
    print(RESULT[:66], "...")
except SzError as err:
    print(f"\nError:\n{err}\n")
