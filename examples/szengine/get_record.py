from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore

data_source_code = "CUSTOMERS"
flags = SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS
instance_name = "Example"
record_id = "1001"
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
    result = sz_engine.get_record(data_source_code, record_id, flags)
    print(f"\n{result}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
