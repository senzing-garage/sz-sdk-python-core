#! /usr/bin/env python3

from szexception import SzException

from . import szdiagnostic

INSTANCE_NAME = "Example"
SECONDS_TO_RUN = 3
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}

try:
    g2_diagnostic = szdiagnostic.G2Diagnostic(INSTANCE_NAME, SETTINGS)
    result = g2_diagnostic.check_database_performance(SECONDS_TO_RUN)
    print(result)
except SzException as err:
    print(err)
