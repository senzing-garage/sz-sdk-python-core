from senzing import SzError

from senzing_core import SzAbstractFactoryCore

instance_name = "Example"
seconds_to_run = 3
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
    result = sz_diagnostic.check_repository_performance(seconds_to_run)
    print(f"\n{result}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
