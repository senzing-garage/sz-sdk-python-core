#! /usr/bin/env python3

from senzing import SzAbstractFactory, SzError

FACTORY_PARAMETERS = {
    "instance_name": "Example",
    "settings": {
        "PIPELINE": {
            "CONFIGPATH": "/etc/opt/senzing",
            "RESOURCEPATH": "/opt/senzing/er/resources",
            "SUPPORTPATH": "/opt/senzing/data",
        },
        "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
    },
    "verbose_logging": 1,
}

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)

except SzError as err:
    print(f"\nError: {err}\n")
