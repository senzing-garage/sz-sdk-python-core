#! /usr/bin/env python3

from senzing import szengine
from senzing.szexception import SzException

END_DATA_SOURCE_CODE = "REFERENCE"
END_RECORD_ID = "2132"
INSTANCE_NAME = "Example"
MAX_DEGREES = 3
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}
START_DATA_SOURCE_CODE = "REFERENCE"
START_RECORD_ID = "2081"

try:
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
    result = sz_engine.find_path_by_record_id(
        START_DATA_SOURCE_CODE,
        START_RECORD_ID,
        END_DATA_SOURCE_CODE,
        END_RECORD_ID,
        MAX_DEGREES,
        # TODO Move these into new example files for find_path
        # NOTE Testing exclusions
        # {"ENTITIES": [{"ENTITY_ID": 800148}]},
        # NOTE Testing required dsrc
        # required_data_sources={"DATA_SOURCES": ["CUSTOMERS"]},
    )
    print(result)
except SzException as err:
    print(err)
