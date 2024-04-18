#! /usr/bin/env python3

from senzing import szconfig, szconfigmanager
from senzing.szexception import SzError

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
    sz_config = szconfig.SzConfig(INSTANCE_NAME, SETTINGS)
    sz_configmgr = szconfigmanager.SzConfigManager(INSTANCE_NAME, SETTINGS)
    config_handle = sz_config.create_config()
    config_str = sz_config.export_config(config_handle)
    config_id = sz_configmgr.add_config(config_str, CONFIG_COMMENT)
    # TODO Might not want the set_default_config_id
    # sz_configmgr.set_default_config_id(config_id)
    print(config_id)
except SzError as err:
    print(err)
