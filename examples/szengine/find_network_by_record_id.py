from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore

build_out_degrees = 1
build_out_max_entities = 10
flags = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS
instance_name = "Example"
max_degrees = 2
record_list = [("CUSTOMERS", "1001"), ("CUSTOMERS", "1009")]
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
    result = sz_engine.find_network_by_record_id(
        record_list, max_degrees, build_out_degrees, build_out_max_entities, flags
    )
    print(f"\n{result}\n")
    import json

    print(json.loads(result))
except SzError as err:
    print(f"\nERROR: {err}\n")
