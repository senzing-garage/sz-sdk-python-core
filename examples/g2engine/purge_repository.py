#! /usr/bin/env python3

from senzing import g2engine
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
    g2_engine = g2engine.G2Engine(MODULE_NAME, INI_PARAMS_DICT)
    # WARNING
    # WARNING - This will remove all loaded and entity resolved data from the Senzing repository, use with caution!
    # WARNING
    g2_engine.purge_repository()
except G2Exception as err:
    print(err)
