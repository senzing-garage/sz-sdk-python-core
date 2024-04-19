#! /usr/bin/env python3

from senzing import szconfig, szconfigmanager
from senzing.szerror import SzError

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
    sz_configmgr = szconfigmanager.SzConfigManager(INSTANCE_NAME, SETTINGS)

    current_config_id = sz_configmgr.get_default_config_id()
    current_config = sz_configmgr.get_config(current_config_id)
    config_handle = sz_config.import_config(current_config)

    result = sz_config.get_data_sources(config_handle)
    sz_config.close_config(config_handle)
    print(result)
except SzError as err:
    print(err)
