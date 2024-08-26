#! /usr/bin/env python3

from senzing import SzEngine, SzError

INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/er/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    # Using get_active_config_id for demonstrations purposes.
    sz_engine = SzEngine(INSTANCE_NAME, SETTINGS)
    config_id = sz_engine.get_active_config_id()
    sz_engine.reinitialize(config_id)
except SzError as err:
    print(f"\nError: {err}\n")
