#! /usr/bin/env python3

from typing import Any, Dict

from senzing import g2config
from senzing.g2exception import G2Exception

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
    g2_config = g2config.G2Config(INSTANCE_NAME, SETTINGS)
    config_handle = g2_config.import_config(json_config_dict)
except G2Exception as err:
    print(err)
