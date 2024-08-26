#! /usr/bin/env python3

from senzing import SzEngine, SzEngineFlags, SzError

END_ENTITY_ID = 1
EXCLUSIONS = [100019]
FLAGS = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS
INSTANCE_NAME = "Example"
MAX_DEGREES = 10
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/er/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
REQUIRED_DATA_SOURCES = None
START_ENTITY_ID = 40

try:
    sz_engine = SzEngine(INSTANCE_NAME, SETTINGS)
    RESULT = sz_engine.find_path_by_entity_id(
        START_ENTITY_ID,
        END_ENTITY_ID,
        MAX_DEGREES,
        EXCLUSIONS,
        REQUIRED_DATA_SOURCES,
        FLAGS,
    )
    print(RESULT)
except SzError as err:
    print(f"\nError: {err}\n")
