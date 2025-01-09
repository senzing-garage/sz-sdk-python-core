#! /usr/bin/env python3

from senzing import SzError

from senzing_core import SzAbstractFactory, SzAbstractFactoryParameters

# The value of config_id is made up, this example will fail if you run it
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
    "config_id": 2787481550,
}

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
except SzError as err:
    print(f"\nFile {__file__}:\nError:\n{err}\n")
