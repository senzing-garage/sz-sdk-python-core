#! /usr/bin/env python3

from szexception import SzException

from . import szconfig, szconfigmgr

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
    g2_config = szconfig.G2Config(INSTANCE_NAME, SETTINGS)
    g2_configmgr = szconfigmgr.G2ConfigMgr(INSTANCE_NAME, SETTINGS)

    current_config_id = g2_configmgr.get_default_config_id()
    current_config = g2_configmgr.get_config(current_config_id)
    config_handle = g2_config.import_config(current_config)

    result = g2_config.get_data_sources(config_handle)
    g2_config.close(config_handle)
    print(result)
except SzException as err:
    print(err)
