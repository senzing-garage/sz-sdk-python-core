#! /usr/bin/env python3

import json

from senzing import g2configmgr, g2diagnostic
from senzing.g2exception import G2Exception

ini_params_dict = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
MODULE_NAME = "Example"

try:
    # Get a configuration ID.
    g2_configmgr = g2configmgr.G2ConfigMgr(MODULE_NAME, json.dumps(ini_params_dict))
    config_id = g2_configmgr.get_default_config_id()

    g2_diagnostic = g2diagnostic.G2Diagnostic()
    g2_diagnostic.init_with_config_id(
        MODULE_NAME, json.dumps(ini_params_dict), config_id
    )
except G2Exception as err:
    print(err)
