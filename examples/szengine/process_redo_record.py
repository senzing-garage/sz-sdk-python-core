#! /usr/bin/env python3

from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactory, SzAbstractFactoryParameters

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
FLAGS = SzEngineFlags.SZ_WITH_INFO

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
    sz_engine = sz_abstract_factory.create_engine()
    while 1:
        redo_record = sz_engine.get_redo_record()
        if not redo_record:
            break
        result = sz_engine.process_redo_record(redo_record, FLAGS)
        print(result)
except SzError as err:
    print(f"\nFile {__file__}:\nError:\n{err}\n")
