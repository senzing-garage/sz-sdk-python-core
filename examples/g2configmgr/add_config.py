#! /usr/bin/env python3

from senzing import g2config, g2configmgr
from senzing.g2exception import G2Exception

CONFIG_COMMENT = "Just an empty example"
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
    g2_config = g2config.G2Config(INSTANCE_NAME, SETTINGS)
    g2_configmgr = g2configmgr.G2ConfigMgr(INSTANCE_NAME, SETTINGS)
    config_handle = g2_config.create()
    config_str = g2_config.save(config_handle)
    config_id = g2_configmgr.add_config(config_str, CONFIG_COMMENT)
    print(config_id)
except G2Exception as err:
    print(err)
