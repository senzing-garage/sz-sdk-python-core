#! /usr/bin/env python3

from senzing import SzError
from using_abstract_2 import try_using_abstract

from senzing_core import SzAbstractFactoryCore, SzAbstractFactoryParametersCore

FACTORY_PARAMETERS: SzAbstractFactoryParametersCore = {
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
    sz_abstract_factory = SzAbstractFactoryCore(**FACTORY_PARAMETERS)
    try_using_abstract(sz_abstract_factory)
except SzError as err:
    print(f"\nERROR: {err}\n")
