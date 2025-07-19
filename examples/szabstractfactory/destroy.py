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
    sz_engine = sz_abstract_factory.create_engine()
    sz_diagnostic = sz_abstract_factory.create_diagnostic()

    # Do work...
except SzError as err:
    print(f"\nERROR: {err}\n")
finally:
    # Destroys the abstract factory and all objects it created, such as sz_engine and sz_diagnostic above
    # If sz_abstract_factory goes out of scope destroy() is automatically called
    sz_abstract_factory.destroy()
