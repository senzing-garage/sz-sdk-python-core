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
    sz_product = sz_abstract_factory.create_product()
    result = sz_product.get_version()
    print(f"\n{result}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
