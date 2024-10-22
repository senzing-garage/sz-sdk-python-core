#! /usr/bin/env python3

from senzing import SzDiagnostic, SzError

INSTANCE_NAME = "Example"
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
    # WARNING
    # WARNING - This will remove all loaded and entity resolved data from the Senzing repository, use with caution!
    # WARNING
    sz_diagnostic.purge_repository()
except SzError as err:
    print(f"\nError: {err}\n")
