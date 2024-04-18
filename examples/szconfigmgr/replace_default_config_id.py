#! /usr/bin/env python3

from senzing import szconfig, szconfigmanager
from senzing.szexception import SzError

CONFIG_COMMENTS = "Just an example"
DATA_SOURCE_CODE = "TEST4"
INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}

# TODO Test this
try:
    sz_config = szconfig.SzConfig(INSTANCE_NAME, SETTINGS)
    sz_configmgr = szconfigmanager.SzConfigManager(INSTANCE_NAME, SETTINGS)

    # Create a new config for the replacement.
    current_config_id = sz_configmgr.get_default_config_id()
    current_config = sz_configmgr.get_config(current_config_id)
    config_handle = sz_config.import_config(current_config)
    sz_config.add_data_source(config_handle, DATA_SOURCE_CODE)
    new_config = sz_config.export_config(config_handle)
    sz_config.close_config(config_handle)
    new_config_id = sz_configmgr.add_config(new_config, CONFIG_COMMENTS)

    sz_configmgr.replace_default_config_id(current_config_id, new_config_id)
    new_current_config_id = sz_configmgr.get_default_config_id()
    print(
        f"Config with ID {current_config_id} was replaced by config with ID {new_current_config_id}"
    )
except SzError as err:
    print(err)
