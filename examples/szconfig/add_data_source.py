#! /usr/bin/env python3

from senzing import SzConfig, SzError

data_source_code = "NAME_OF_DATASOURCE"
instance_name = "Example"
settings = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_config = SzConfig(instance_name, settings)
    config_handle = sz_config.create_config()
    RESULT = sz_config.add_data_source(config_handle, data_source_code)
    sz_config.close_config(config_handle)
    print(RESULT[:66], "...")
except SzError as err:
    print(f"\nError:\n{err}\n")
