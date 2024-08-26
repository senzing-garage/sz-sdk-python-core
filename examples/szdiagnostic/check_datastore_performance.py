#! /usr/bin/env python3

from senzing import SzDiagnostic, SzError

INSTANCE_NAME = "Example"
SECONDS_TO_RUN = 3
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/er/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_diagnostic = SzDiagnostic(INSTANCE_NAME, SETTINGS)
    RESULT = sz_diagnostic.check_datastore_performance(SECONDS_TO_RUN)
    print(RESULT)
except SzError as err:
    print(f"\nError: {err}\n")
