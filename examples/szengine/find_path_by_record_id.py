#! /usr/bin/env python3

from senzing import SzEngine, SzEngineFlags, SzError

END_DATA_SOURCE_CODE = "CUSTOMERS"
END_RECORD_ID = "1009"
# TODO
# EXCLUSIONS = ""
EXCLUSIONS = [("CUSTOMERS", "999")]
# EXCLUSIONS = None
FLAGS = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS
INSTANCE_NAME = "Example"
MAX_DEGREES = 10
# REQUIRED_DATA_SOURCES = ""
# REQUIRED_DATA_SOURCES = ["REFERENCE\n", "CUSTOMERS\r\n😂"]
REQUIRED_DATA_SOURCES = ["REFERENCE", "CUSTOMERS"]
# REQUIRED_DATA_SOURCES = ["ANT"]
# REQUIRED_DATA_SOURCES = None
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
START_DATA_SOURCE_CODE = "CUSTOMERS"
START_RECORD_ID = "1001"

try:
    sz_engine = SzEngine(INSTANCE_NAME, SETTINGS)
    RESULT = sz_engine.find_path_by_record_id(
        START_DATA_SOURCE_CODE,
        START_RECORD_ID,
        END_DATA_SOURCE_CODE,
        END_RECORD_ID,
        MAX_DEGREES,
        EXCLUSIONS,
        REQUIRED_DATA_SOURCES,
        FLAGS,
    )
    print(RESULT)
except SzError as err:
    print(f"\nError:\n{err}\n")
