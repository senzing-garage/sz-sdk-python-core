#! /usr/bin/env python3

import json

from senzing import g2diagnostic
from senzing.g2exception import G2Exception

INI_PARAMS_DICT = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
MODULE_NAME = "Example"

try:
    G2_DIAGNOSIS = g2diagnostic.G2Diagnostic()
    G2_DIAGNOSIS.init(MODULE_NAME, json.dumps(INI_PARAMS_DICT))

    # Do work.

    G2_DIAGNOSIS.destroy()
except G2Exception as err:
    print(err)
