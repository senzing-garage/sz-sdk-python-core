#! /usr/bin/env python3

from senzing import szdiagnostic
from senzing.szexception import SzException

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
    sz_diagnostic = szdiagnostic.SzDiagnostic(INSTANCE_NAME, SETTINGS)
    result = sz_diagnostic.check_database_performance(SECONDS_TO_RUN)
    print(result)
except SzException as err:
    print(err)
