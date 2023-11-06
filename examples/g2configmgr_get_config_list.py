#! /usr/bin/env python3

import json

from senzing import g2configmgr
from senzing.g2exception import G2Exception

ENGINE_CONFIGURATION = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
ENGINE_MODULE_NAME = "EXAMPLE"

try:
    G2_CONFIGMGR = g2configmgr.G2ConfigMgr(
        ENGINE_MODULE_NAME, json.dumps(ENGINE_CONFIGURATION)
    )
    CONFIGURATION_LIST = G2_CONFIGMGR.get_config_list()
    print(CONFIGURATION_LIST)
except G2Exception as err:
    print(err)
