#! /usr/bin/env python3

from senzing import szdiagnostic
from senzing.szexception import SzException

INSTANCE_NAME = "Example"
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
    # WARNING
    # WARNING - This will remove all loaded and entity resolved data from the Senzing repository, use with caution!
    # WARNING
    sz_diagnostic.purge_repository()
except SzException as err:
    print(err)
