#! /usr/bin/env python3

from senzing import SzError, szengine

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
    sz_engine = szengine.SzEngine()
    sz_engine.initialize(INSTANCE_NAME, SETTINGS)
    active_config_id = sz_engine.get_active_config_id()
    sz_engine.destroy()

    sz_engine.initialize(INSTANCE_NAME, SETTINGS, config_id=active_config_id)
    sz_engine.destroy()
except SzError as err:
    print(f"\nError:\n{err}\n")
