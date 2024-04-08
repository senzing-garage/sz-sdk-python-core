#! /usr/bin/env python3


from senzing import szconfig
from szexception import SzException

SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
MODULE_NAME = "Example"

try:
    sz_config = szconfig.SzConfig(MODULE_NAME, SETTINGS)
    config_handle = sz_config.create()  # Create first in-memory.
    json_config = sz_config.export_config(config_handle)  # Save in-memory to string.
    sz_config.close(config_handle)
    print(json_config)
except SzException as err:
    print(err)
