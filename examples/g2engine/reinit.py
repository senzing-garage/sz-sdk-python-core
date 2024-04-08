#! /usr/bin/env python3


from szexception import SzException

from . import szengine

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
    g2_engine = szengine.G2Engine(INSTANCE_NAME, SETTINGS)
    # Using get_active_config_id for demonstrations purposes
    active_config_id = g2_engine.get_active_config_id()
    g2_engine.reinitialize(active_config_id)
except SzException as err:
    print(err)
