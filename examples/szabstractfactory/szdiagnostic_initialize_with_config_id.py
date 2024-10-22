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

except SzError as err:
    print(f"\nError: {err}\n")


#! /usr/bin/env python3

from senzing import SzConfigManager, SzDiagnostic, SzError

INSTANCE_NAME = "Example"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_configmanager = SzConfigManager(INSTANCE_NAME, SETTINGS)
    config_id = sz_configmanager.get_default_config_id()
    sz_diagnostic = SzDiagnostic(INSTANCE_NAME, SETTINGS, config_id=config_id)
except SzError as err:
    print(f"\nError: {err}\n")
