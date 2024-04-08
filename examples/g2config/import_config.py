#! /usr/bin/env python3

from typing import Any, Dict

from szexception import SzException

from . import szconfig

INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
# TODO Change to use config manager to get a default config
json_config_dict: Dict[str, Any] = (
    {}
)  # Naturally, this would be a full Senzing configuration.


try:
    g2_config = szconfig.G2Config(INSTANCE_NAME, SETTINGS)
    config_handle = g2_config.import_config(json_config_dict)
except SzException as err:
    print(err)
