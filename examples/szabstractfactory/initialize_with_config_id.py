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
}

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
    sz_configmanager = sz_abstract_factory.create_sz_configmanager()
    config_id = sz_configmanager.get_default_config_id()
    sz_abstract_factory.reinitialize(config_id)

except SzError as err:
    print(f"\nError: {err}\n")
