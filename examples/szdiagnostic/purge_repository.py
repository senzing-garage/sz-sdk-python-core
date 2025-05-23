from senzing import SzError

from senzing_core import SzAbstractFactoryCore

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
    sz_diagnostic = sz_abstract_factory.create_diagnostic()
    # WARNING
    # WARNING - This will remove all loaded and entity resolved data from the Senzing repository, use with caution!
    # WARNING - Uncomment the purge_repository() call below to complete a purge
    # WARNING

    # sz_diagnostic.purge_repository()
except SzError as err:
    print(f"\nERROR: {err}\n")
