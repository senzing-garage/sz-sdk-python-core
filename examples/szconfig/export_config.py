#! /usr/bin/env python3


from senzing import szconfig
from senzing.szerror import SzError

SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
INSTANCE_NAME = "Example"

try:
    sz_config = szconfig.SzConfig(INSTANCE_NAME, SETTINGS)
    config_handle = sz_config.create_config()  # Create first in-memory.
    config = sz_config.export_config(config_handle)  # Save in-memory to string.
    sz_config.close_config(config_handle)
    print(config)
except SzError as err:
    print(err)
