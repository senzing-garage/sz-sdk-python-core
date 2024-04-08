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
    config_handle = sz_config.create()

    # Do work.

    sz_config.close(config_handle)
except SzException as err:
    print(err)
