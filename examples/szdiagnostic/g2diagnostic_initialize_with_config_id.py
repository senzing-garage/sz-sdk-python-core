#! /usr/bin/env python3


from senzing import szconfigmanager, szdiagnostic
from senzing.szerror import SzError

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
    # Get a configuration ID.
    sz_configmgr = szconfigmanager.SzConfigManager(INSTANCE_NAME, SETTINGS)
    config_id = sz_configmgr.get_default_config_id()

    sz_diagnostic = szdiagnostic.SzDiagnostic(
        INSTANCE_NAME, SETTINGS, config_id=config_id
    )
except SzError as err:
    print(err)
