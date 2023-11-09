#! /usr/bin/env python3

import json
from typing import Any, Dict

from senzing import g2config, g2configmgr
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
config_str_dict: Dict[
    str, Any
] = {}  # Naturally, this would be a full Senzing configuration.
COMMENT = "Just an empty example"

try:
    g2_config = g2config.G2Config(MODULE_NAME, json.dumps(ini_params_dict))
    g2_configmgr = g2configmgr.G2ConfigMgr(MODULE_NAME, json.dumps(ini_params_dict))

    # Create a new config.

    config_handle = g2_config.create()
    input_json_dict = {"DSRC_CODE": "REPLACE_DEFAULT_CONFIG_ID"}
    g2_config.add_data_source(config_handle, json.dumps(input_json_dict))
    json_config = g2_config.save(config_handle)
    NEW_CONFIG_ID = g2_configmgr.add_config(json_config, "Test")

    old_config_id = g2_configmgr.get_default_config_id()
    g2_configmgr.replace_default_config_id(old_config_id, NEW_CONFIG_ID)
except G2Exception as err:
    print(err)
