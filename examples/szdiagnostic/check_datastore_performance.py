#! /usr/bin/env python3

from senzing import SzError

from senzing_core import SzAbstractFactoryCore

INSTANCE_NAME = "Example"
SECONDS_TO_RUN = 3
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/er/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}


try:
    sz_abstract_factory = SzAbstractFactoryCore(INSTANCE_NAME, SETTINGS)
    sz_diagnostic = sz_abstract_factory.create_diagnostic()
    result = sz_diagnostic.check_datastore_performance(SECONDS_TO_RUN)
    print(f"\n{result}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
