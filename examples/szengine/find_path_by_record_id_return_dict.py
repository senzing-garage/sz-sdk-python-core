#! /usr/bin/env python3

from senzing import szengine
from szexception import SzException

END_DATA_SOURCE_CODE = "REFERENCE"
INSTANCE_NAME = "Example"
END_RECORD_ID = "2132"
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
    result = sz_engine.find_path_by_record_id_return_dict(
        START_DATA_SOURCE_CODE,
        START_RECORD_ID,
        END_DATA_SOURCE_CODE,
        END_RECORD_ID,
        MAX_DEGREES,
    )
    print(result)
except SzException as err:
    print(err)
