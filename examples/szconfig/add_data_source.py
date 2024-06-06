#! /usr/bin/env python3

import json

from senzing import SzConfig, SzError

# DATA_SOURCE_CODE = "éanty\r😂"
DATA_SOURCE_CODE = "TEST2"
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

    dsrc = json.dumps(dict(text=DATA_SOURCE_CODE)["text"])
    RESULT = sz_config.add_data_source(config_handle, DATA_SOURCE_CODE)
    # TODO
    # RESULT2 = sz_config.get_data_sources(config_handle)
    sz_config.close_config(config_handle)
    print(RESULT)
    # print(str(RESULT2))
except SzError as err:
    print(f"\nError:\n{err}\n")
