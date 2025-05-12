from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore

data_source_code_1 = "CUSTOMERS"
data_source_code_2 = "CUSTOMERS"
flags = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS
instance_name = "Example"
record_id_1 = "1001"
record_id_2 = "1002"
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
    result = sz_engine.why_records(
        data_source_code_1,
        record_id_1,
        data_source_code_2,
        record_id_2,
        flags,
    )
    print(f"\n{result}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
