#! /usr/bin/env python3

import json

from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactory, SzAbstractFactoryParameters

ATTRIBUTES = json.dumps({"NAME_FULL": "BOB SMITH", "EMAIL_ADDRESS": "bsmith@work.com"})
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
FLAGS = SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS
SEARCH_PROFILE = ""

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
    sz_engine = sz_abstract_factory.create_engine()
    RESULT = sz_engine.search_by_attributes(ATTRIBUTES, FLAGS, SEARCH_PROFILE)
    print(f"\nFile {__file__}:\n{RESULT}\n")
except SzError as err:
    print(f"\nFile {__file__}:\nError:\n{err}\n")
