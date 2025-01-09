#! /usr/bin/env python3

from senzing import SzError

from senzing_core import SzAbstractFactory, SzAbstractFactoryParameters

FACTORY_PARAMETERS: SzAbstractFactoryParameters = {
    "instance_name": "Example",
    "settings": {
        "PIPELINE": {
            "CONFIGPATH": "/etc/opt/senzing",
            "RESOURCEPATH": "/opt/senzing/er/resources",
            "SUPPORTPATH": "/opt/senzing/data",
        },
        "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
    },
}

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
    sz_diagnostic = sz_abstract_factory.create_diagnostic()
    # WARNING
    # WARNING - This will remove all loaded and entity resolved data from the Senzing repository, use with caution!
    # WARNING
    if (
        input(
            "WARNING: This will remove all loaded and entity resolved data from the Senzing repository, type YESPURGESENZING to continue and purge! "
        )
        == "YESPURGESENZING"
    ):
        sz_diagnostic.purge_repository()
except SzError as err:
    print(f"\nFile {__file__}:\nError:\n{err}\n")
