#! /usr/bin/env python3

from senzing import SzAbstractFactory, SzAbstractFactoryParameters, SzError

FACTORY_PARAMETERS: SzAbstractFactoryParameters = {
    "instance_name": "Example",
    "settings": {
        "PIPELINE": {
            "CONFIGPATH": "/etc/opt/senzing",
            "RESOURCEPATH": "/opt/senzing/er/resources",
            "SUPPORTPATH": "/opt/senzing/data",
        },
        "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
    },
}
SECONDS_TO_RUN = 3

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
    sz_diagnostic = sz_abstract_factory.create_sz_diagnostic()
    RESULT = sz_diagnostic.check_datastore_performance(SECONDS_TO_RUN)
    print(RESULT)
except SzError as err:
    print(f"\nError in {__file__}: {err}\n")
