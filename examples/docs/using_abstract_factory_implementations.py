import json

from senzing import SzAbstractFactory, SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore


def perform_senzing_search(search_abstract_factory: SzAbstractFactory, search_attributes: str) -> str:
    """Example Senzing search using Abstract Base Class SzAbstractFactory."""
    sz_engine = search_abstract_factory.create_engine()
    flags = SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS
    search_profile = ""
    return sz_engine.search_by_attributes(search_attributes, flags, search_profile)


# Example using SzAbstractFactoryCore implementation class.

try:
    instance_name = "Example"
    settings = {
        "PIPELINE": {
            "CONFIGPATH": "/etc/opt/senzing",
            "RESOURCEPATH": "/opt/senzing/er/resources",
            "SUPPORTPATH": "/opt/senzing/data",
        },
        "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
    }
    sz_abstract_factory = SzAbstractFactoryCore(instance_name, settings)
    attributes = json.dumps({"NAME_FULL": "Bob Smith", "EMAIL_ADDRESS": "bsmith@work.com"})
    search_results = perform_senzing_search(sz_abstract_factory, attributes)
    print(search_results)
except SzError as err:
    print(f"\nERROR: {err}\n")
