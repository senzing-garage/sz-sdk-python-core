from typing import List

from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore

avoid_entity_ids: List[int] = []
end_entity_id = 400215
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
start_entity_id = 1

try:
    sz_abstract_factory = SzAbstractFactoryCore(instance_name, settings)
    sz_engine = sz_abstract_factory.create_engine()
    result = sz_engine.find_path_by_entity_id(
        start_entity_id,
        end_entity_id,
        max_degrees,
        avoid_entity_ids,
        required_data_sources,
        flags,
    )
    print(f"\n{result}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
