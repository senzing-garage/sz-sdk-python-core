#! /usr/bin/env python3

from senzing import szconfig
from szexception import SzException

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
    sz_config = szconfig.SzConfig(INSTANCE_NAME, SETTINGS)
    config_handle_1 = sz_config.create()  # Create first in-memory.
    json_config = sz_config.export_config(config_handle_1)  # Save in-memory to string.
    config_handle_2 = sz_config.import_config(json_config)  # Create second in-memory.
    sz_config.close(config_handle_1)
    sz_config.close(config_handle_2)
except SzException as err:
    print(err)
