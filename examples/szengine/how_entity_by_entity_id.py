#! /usr/bin/env python3

from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore

ENTITY_ID = 1
FLAGS = SzEngineFlags.SZ_HOW_ENTITY_DEFAULT_FLAGS
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
    sz_engine = sz_abstract_factory.create_engine()
    result = sz_engine.how_entity_by_entity_id(ENTITY_ID, FLAGS)
    print(f"\n{result}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
