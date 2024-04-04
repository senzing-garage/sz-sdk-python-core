#! /usr/bin/env python3

from senzing import g2config, g2configmgr
from senzing.g2exception import G2Exception

CONFIG_COMMENT = "Added new datasource"
DATA_SOURCE_CODE = "TEST12"
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

    current_config_id = g2_configmgr.get_default_config_id()
    current_config = g2_configmgr.get_config(current_config_id)
    config_handle = g2_config.load(current_config)

    result = g2_config.add_data_source(config_handle, DATA_SOURCE_CODE)
    new_config = g2_config.save(config_handle)
    g2_config.close(config_handle)

    new_config_id = g2_configmgr.add_config(new_config, CONFIG_COMMENT)
    g2_configmgr.set_default_config_id(new_config_id)

    print(result)
except G2Exception as err:
    print(err)
