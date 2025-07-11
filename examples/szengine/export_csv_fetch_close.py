from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore

csv_column_list = (
    "RESOLVED_ENTITY_ID,RELATED_ENTITY_ID,RESOLVED_ENTITY_NAME,MATCH_LEVEL,MATCH_KEY,DATA_SOURCE,RECORD_ID"
)
flags = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS
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
    export_handle = sz_engine.export_csv_entity_report(csv_column_list, flags)
    while True:
        fragment = sz_engine.fetch_next(export_handle)
        if not fragment:
            break
        print(fragment, end="")
    sz_engine.close_export_report(export_handle)
except SzError as err:
    print(f"\nERROR: {err}\n")
