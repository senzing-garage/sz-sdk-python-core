#! /usr/bin/env python3

from senzing import SzConfig, SzError

DATA_SOURCE_CODE = "NAME_OF_DATASOURCE"
INSTANCE_NAME = "Example"
settings = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_config = SzConfig(INSTANCE_NAME, settings)
    config_handle = sz_config.create_config()
    RESULT = sz_config.add_data_source(config_handle, DATA_SOURCE_CODE)
    sz_config.close_config(config_handle)
    print(RESULT)
except SzError as err:
    print(f"\nError:\n{err}\n")
