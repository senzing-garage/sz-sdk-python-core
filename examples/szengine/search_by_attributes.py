import json

from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore

attributes = json.dumps({"NAME_FULL": "Bob Smith", "EMAIL_ADDRESS": "bsmith@work.com"})
flags = SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS
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
    result = sz_engine.search_by_attributes(attributes, flags)
    print(f"\n{result}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
