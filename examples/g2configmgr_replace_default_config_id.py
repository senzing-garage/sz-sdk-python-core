#! /usr/bin/env python3

import json
from typing import Any, Dict

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
CONFIGURATION: Dict[
    str, Any
] = {}  # Naturally, this would be a full Senzing configuration.
COMMENT = "Just an empty example"

try:
    G2_CONFIGMGR = g2configmgr.G2ConfigMgr(
        ENGINE_MODULE_NAME, json.dumps(ENGINE_CONFIGURATION)
    )
    CONFIG_HANDLE_OLD = G2_CONFIGMGR.get_default_config_id()
    CONFIG_HANDLE_NEW = G2_CONFIGMGR.add_config(json.dumps(CONFIGURATION), COMMENT)
    G2_CONFIGMGR.replace_default_config_id(CONFIG_HANDLE_OLD, CONFIG_HANDLE_NEW)
except G2Exception as err:
    print(err)
