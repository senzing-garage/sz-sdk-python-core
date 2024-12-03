#! /usr/bin/env python3

from senzing_core import SzAbstractFactory, SzAbstractFactoryParameters, SzError

DATA_SOURCE_CODE = "NAME_OF_DATASOURCE"
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
    sz_product = sz_abstract_factory.create_product()
except SzError as err:
    print(f"\nError:\n{err}\n")
