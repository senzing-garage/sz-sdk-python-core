#! /usr/bin/env python3

from senzing import szdiagnostic
from senzing.szexception import SzError

INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}

# Example 1

try:
    sz_diagnostic1 = szdiagnostic.SzDiagnostic(INSTANCE_NAME, SETTINGS)
except SzError as err:
    print(err)

# Example 2

try:
    sz_diagnostic2 = szdiagnostic.SzDiagnostic()
    sz_diagnostic2.initialize(INSTANCE_NAME, SETTINGS)
    sz_diagnostic2.destroy()
except SzError as err:
    print(err)
