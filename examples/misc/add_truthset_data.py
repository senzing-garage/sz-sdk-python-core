from senzing import SZ_WITHOUT_INFO, SzError
from senzing_truthset import (
    TRUTHSET_CUSTOMER_RECORDS,
    TRUTHSET_REFERENCE_RECORDS,
    TRUTHSET_WATCHLIST_RECORDS,
)

from senzing_core import SzAbstractFactoryCore

instance_name = "Example"
record_sets = [
    TRUTHSET_CUSTOMER_RECORDS,
    TRUTHSET_REFERENCE_RECORDS,
    TRUTHSET_WATCHLIST_RECORDS,
]
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
    for record_set in record_sets:
        for record in record_set.values():
            sz_engine.add_record(
                record.get("DataSource"),
                record.get("Id"),
                record.get("Json"),
                SZ_WITHOUT_INFO,
            )
except SzError as err:
    print(f"\nERROR: {err}\n")
