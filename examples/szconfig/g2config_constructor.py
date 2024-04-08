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
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}

# Example 1

try:
    sz_config1 = szconfig.SzConfig(INSTANCE_NAME, SETTINGS)
except SzException as err:
    print(err)

# Example 2

try:
    sz_config2 = szconfig.SzConfig()
    sz_config2.initialize(INSTANCE_NAME, SETTINGS)
    sz_config2.destroy()
except SzException as err:
    print(err)
