#! /usr/bin/env python3

from szexception import SzException

from . import szconfig

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
    g2_config = szconfig.G2Config()
    g2_config.initialize(INSTANCE_NAME, SETTINGS)

    # Do work.

    g2_config.destroy()
except SzException as err:
    print(err)
