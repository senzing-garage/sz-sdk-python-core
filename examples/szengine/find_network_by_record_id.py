#! /usr/bin/env python3

from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactory, SzAbstractFactoryParameters

BUILD_OUT_DEGREES = 1
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
FLAGS = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS
MAX_DEGREES = 2
MAX_ENTITIES = 10
RECORD_LIST = [("CUSTOMERS", "1001"), ("CUSTOMERS", "1009")]

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
    sz_engine = sz_abstract_factory.create_engine()
    RESULT = sz_engine.find_network_by_record_id(RECORD_LIST, MAX_DEGREES, BUILD_OUT_DEGREES, MAX_ENTITIES, FLAGS)
    print(f"\nFile {__file__}:\n{RESULT}\n")
except SzError as err:
    print(f"\nFile {__file__}:\nError:\n{err}\n")
