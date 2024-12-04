#! /usr/bin/env python3

from senzing_core import SzAbstractFactory, SzAbstractFactoryParameters, SzError

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
    sz_config = sz_abstract_factory.create_config()
    sz_configmanager = sz_abstract_factory.create_configmanager()
    config_id = sz_configmanager.get_default_config_id()
    CONFIG_DEFINITION = sz_configmanager.get_config(config_id)
    config_handle = sz_config.import_config(CONFIG_DEFINITION)
except SzError as err:
    print(f"\nFile {__file__}:\nError:\n{err}\n")
