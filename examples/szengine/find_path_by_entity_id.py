#! /usr/bin/env python3

from typing import List

from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore

AVOID_ENTITY_IDS: List[int] = []
END_ENTITY_ID = 4
FLAGS = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS
INSTANCE_NAME = "Example"
MAX_DEGREES = 2
REQUIRED_DATA_SOURCES: List[str] = []
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/er/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
START_ENTITY_ID = 1

try:
    sz_abstract_factory = SzAbstractFactoryCore(INSTANCE_NAME, SETTINGS)
    sz_engine = sz_abstract_factory.create_engine()
    RESULT = sz_engine.find_path_by_entity_id(
        START_ENTITY_ID,
        END_ENTITY_ID,
        MAX_DEGREES,
        AVOID_ENTITY_IDS,
        REQUIRED_DATA_SOURCES,
        FLAGS,
    )
    print(f"\n{RESULT}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
