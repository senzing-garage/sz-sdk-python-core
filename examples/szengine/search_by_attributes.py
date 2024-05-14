#! /usr/bin/env python3

from senzing import SzEngine, SzEngineFlags, SzError

ATTRIBUTES = {"NAME_FULL": "BOB SMITH", "EMAIL_ADDRESS": "bsmith@work.com"}
FLAGS = SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS
INSTANCE_NAME = "Example"
SEARCH_PROFILE = ""
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_engine = SzEngine(INSTANCE_NAME, SETTINGS)
    RESULT = sz_engine.search_by_attributes(ATTRIBUTES, SEARCH_PROFILE, FLAGS)
    print(RESULT)
except SzError as err:
    print(f"\nError:\n{err}\n")
