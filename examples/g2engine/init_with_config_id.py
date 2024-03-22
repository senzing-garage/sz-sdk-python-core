#! /usr/bin/env python3

from senzing import g2engine
from senzing.g2exception import G2Exception

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
    g2_engine = g2engine.G2Engine()
    g2_engine.initialize(INSTANCE_NAME, SETTINGS)
    # Using get_active_config_id for demonstrations purposes
    active_config_id = g2_engine.get_active_config_id()
    g2_engine.initialize(INSTANCE_NAME, SETTINGS, active_config_id)
    g2_engine.destroy()
except G2Exception as err:
    print(err)
