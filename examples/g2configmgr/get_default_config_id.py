#! /usr/bin/env python3

from senzing import g2configmgr
from senzing.g2exception import G2Exception

INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}

try:
    g2_configmgr = g2configmgr.G2ConfigMgr(INSTANCE_NAME, SETTINGS)
    config_id = g2_configmgr.get_default_config_id()
    print(config_id)
except G2Exception as err:
    print(err)
