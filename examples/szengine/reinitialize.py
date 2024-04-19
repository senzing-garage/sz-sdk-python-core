#! /usr/bin/env python3


from senzing import szengine
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
    # Using get_active_config_id for demonstrations purposes
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    active_config_id = sz_engine.get_active_config_id()
    sz_engine.reinitialize(active_config_id)
except SzError as err:
    print(err)
