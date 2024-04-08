#! /usr/bin/env python3

from szexception import SzException

from . import szdiagnostic

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
    g2_diagnostic = szdiagnostic.G2Diagnostic(INSTANCE_NAME, SETTINGS)
except SzException as err:
    print(err)

# Example 2

try:
    g2_diagnostic = szdiagnostic.G2Diagnostic()
    g2_diagnostic.initialize(INSTANCE_NAME, SETTINGS)
except SzException as err:
    print(err)
