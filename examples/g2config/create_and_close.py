#! /usr/bin/env python3

from senzing import g2config
from senzing.g2exception import G2Exception

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
    g2_config = g2config.G2Config(INSTANCE_NAME, SETTINGS)
    config_handle = g2_config.create()

    # Do work.

    g2_config.close(config_handle)
except G2Exception as err:
    print(err)
