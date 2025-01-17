#! /usr/bin/env python3

from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore

ATTRIBUTES = '{"NAME_FULL": "BOB SMITH", "EMAIL_ADDRESS": "bsmith@work.com"}'
FLAGS = SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS
INSTANCE_NAME = "Example"
SEARCH_PROFILE = ""
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
    sz_engine = sz_abstract_factory.create_engine()
    RESULT = sz_engine.search_by_attributes(ATTRIBUTES, FLAGS, SEARCH_PROFILE)
    print(f"\n{RESULT}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
