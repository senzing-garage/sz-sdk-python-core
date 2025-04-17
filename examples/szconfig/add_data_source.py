#! /usr/bin/env python3

from senzing import SzError

from senzing_core import SzAbstractFactoryCore

INSTANCE_NAME = "Example"
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
    sz_configmanager = sz_abstract_factory.create_configmanager()
    DATA_SOURCE_CODE = "NAME_OF_DATASOURCE"
    sz_config = sz_configmanager.create_config_from_template()
    RESULT = sz_config.add_data_source(DATA_SOURCE_CODE)
    print(f"\n{RESULT}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
