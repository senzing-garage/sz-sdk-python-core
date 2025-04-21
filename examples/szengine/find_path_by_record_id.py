from typing import List, Tuple

from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore

avoid_record_keys: List[Tuple[str, str]] = []
end_data_source_code = "CUSTOMERS"
end_record_id = "1009"
flags = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS
instance_name = "Example"
max_degrees = 2
required_data_sources: List[str] = []
settings = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/er/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
start_data_source_code = "CUSTOMERS"
start_record_id = "1001"

try:
    sz_abstract_factory = SzAbstractFactoryCore(instance_name, settings)
    sz_engine = sz_abstract_factory.create_engine()
    result = sz_engine.find_path_by_record_id(
        start_data_source_code,
        start_record_id,
        end_data_source_code,
        end_record_id,
        max_degrees,
        avoid_record_keys,
        required_data_sources,
        flags,
    )
    print(f"\n{result}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
