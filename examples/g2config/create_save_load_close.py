#! /usr/bin/env python3

import json

from szexception import SzException

from . import szconfig

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
    g2_config = szconfig.G2Config(MODULE_NAME, json.dumps(ini_params_dict))
    config_handle_1 = g2_config.create()  # Create first in-memory.
    json_config = g2_config.save(config_handle_1)  # Save in-memory to string.
    config_handle_2 = g2_config.load(json_config)  # Create second in-memory.
    g2_config.close(config_handle_1)
    g2_config.close(config_handle_2)
except SzException as err:
    print(err)
