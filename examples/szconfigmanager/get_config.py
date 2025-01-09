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
    config_id = sz_configmanager.get_default_config_id()
    CONFIG_DEFINITION = sz_configmanager.get_config(config_id)
    print(f"\nFile {__file__}:\n{CONFIG_DEFINITION}\n")
except SzError as err:
    print(f"\nFile {__file__}:\nError:\n{err}\n")
