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
}

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
    sz_configmanager = sz_abstract_factory.create_configmanager()
    CONFIG_LIST = sz_configmanager.get_configs()
    print(f"\nFile {__file__}:\n{CONFIG_LIST}\n")
except SzError as err:
    print(f"\nFile {__file__}:\nError:\n{err}\n")
