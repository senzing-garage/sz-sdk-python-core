#! /usr/bin/env python3

from senzing import SzDiagnostic, SzError

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
    sz_diagnostic1 = SzDiagnostic(INSTANCE_NAME, SETTINGS)
except SzError as err:
    print(f"\nError:\n{err}\n")

# Example 2

try:
    sz_diagnostic2 = SzDiagnostic()
    sz_diagnostic2.initialize(INSTANCE_NAME, SETTINGS)
    sz_diagnostic2.destroy()
except SzError as err:
    print(f"\nError:\n{err}\n")
