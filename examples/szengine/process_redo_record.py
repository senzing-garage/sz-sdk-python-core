from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore

flags = SzEngineFlags.SZ_WITH_INFO
instance_name = "Example"
settings = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/er/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_abstract_factory = SzAbstractFactoryCore(instance_name, settings)
    sz_engine = sz_abstract_factory.create_engine()
    while True:
        redo_record = sz_engine.get_redo_record()
        if not redo_record:
            break
        result = sz_engine.process_redo_record(redo_record, flags)
        print(result)
except SzError as err:
    print(f"\nERROR: {err}\n")
