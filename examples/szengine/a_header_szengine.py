#! /usr/bin/env python3

"""
Simply a header used in development.
"""

from typing import List, Tuple

from senzing import (
    SZ_WITHOUT_INFO,
    SzAbstractFactory,
    SzAbstractFactoryParameters,
    SzEngine,
)
from senzing_truthset import (
    TRUTHSET_CUSTOMER_RECORDS,
    TRUTHSET_REFERENCE_RECORDS,
    TRUTHSET_WATCHLIST_RECORDS,
)

data_sources = {
    "CUSTOMERS": TRUTHSET_CUSTOMER_RECORDS,
    "REFERENCE": TRUTHSET_REFERENCE_RECORDS,
    "WATCHLIST": TRUTHSET_WATCHLIST_RECORDS,
}
FACTORY_PARAMETERS: SzAbstractFactoryParameters = {
    "instance_name": "Example1",
    "settings": {
        "PIPELINE": {
            "CONFIGPATH": "/etc/opt/senzing",
            "RESOURCEPATH": "/opt/senzing/er/resources",
            "SUPPORTPATH": "/opt/senzing/data",
        },
        "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
    },
}
test_records: List[Tuple[str, str]] = [
    ("CUSTOMERS", "1001"),
    ("CUSTOMERS", "1002"),
    ("CUSTOMERS", "1003"),
    ("CUSTOMERS", "1009"),
]

# -----------------------------------------------------------------------------
# Internal functions
# -----------------------------------------------------------------------------


def add_records(
    sz_engine_local: SzEngine, record_id_list: List[Tuple[str, str]]
) -> None:
    """Add all of the records in the list."""
    flags = SZ_WITHOUT_INFO
    for record_identification in record_id_list:
        datasource = record_identification[0]
        record_id = record_identification[1]
        record = data_sources.get(datasource, {}).get(record_id, {})
        sz_engine_local.add_record(
            record.get("DataSource", ""),
            record.get("Id", ""),
            record.get("Json", ""),
            flags,
        )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

print("\n---- szengine --------------------------------------------------------\n")

sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
sz_engine = sz_engine = sz_abstract_factory.create_sz_engine()
add_records(sz_engine, test_records)
