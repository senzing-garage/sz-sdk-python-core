#! /usr/bin/env python3

from senzing import SzError

from senzing_core import SzAbstractFactory, SzAbstractFactoryParameters

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
    "verbose_logging": 1,
}

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
    # Create an engine to show debug output
    sz_abstract_factory.create_engine()
except SzError as err:
    print(f"\nFile {__file__}:\nError:\n{err}\n")
