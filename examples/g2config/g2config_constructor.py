#! /usr/bin/env python3

from szexception import SzException

from . import szconfig

INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}

# Example 1

try:
    g2_config = szconfig.G2Config(INSTANCE_NAME, SETTINGS)
except SzException as err:
    print(err)

# Example 2

try:
    g2_config = szconfig.G2Config()
    g2_config.initialize(INSTANCE_NAME, SETTINGS)
except SzException as err:
    print(err)
