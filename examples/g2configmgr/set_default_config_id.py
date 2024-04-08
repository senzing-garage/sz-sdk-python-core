#! /usr/bin/env python3

from szexception import SzException

from . import szconfig, szconfigmgr

CONFIG_COMMENT = "Just an example"
DATA_SOURCE_CODE = "TEST20"
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
    g2_config = szconfig.G2Config(INSTANCE_NAME, SETTINGS)
    g2_configmgr = szconfigmgr.G2ConfigMgr(INSTANCE_NAME, SETTINGS)

    # Create a new config.

    config_handle = g2_config.create()
    g2_config.add_data_source(config_handle, DATA_SOURCE_CODE)
    json_config = g2_config.save(config_handle)
    config_id = g2_configmgr.add_config(json_config, CONFIG_COMMENT)
    g2_configmgr.set_default_config_id(config_id)
except SzException as err:
    print(err)
