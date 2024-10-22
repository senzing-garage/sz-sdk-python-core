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

try:
    sz_diagnostic = SzDiagnostic(INSTANCE_NAME, SETTINGS, verbose_logging=1)
except SzError as err:
    print(err)
