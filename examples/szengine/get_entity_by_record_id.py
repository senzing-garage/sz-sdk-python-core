from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore

data_source_code = "CUSTOMERS"
flags = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS
instance_name = "Example"
settings = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/er/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
record_id = "1001"

try:
    sz_abstract_factory = SzAbstractFactoryCore(instance_name, settings)
    sz_engine = sz_abstract_factory.create_engine()
    result = sz_engine.get_entity_by_record_id(data_source_code, record_id, flags)
    print(f"\n{result}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
