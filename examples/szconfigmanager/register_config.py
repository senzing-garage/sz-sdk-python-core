from senzing import SzError

from senzing_core import SzAbstractFactoryCore

config_comment = "Just an empty example"
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
    sz_configmanager = sz_abstract_factory.create_configmanager()
    sz_config = sz_configmanager.create_config_from_template()
    config_definition = sz_config.export()
    config_id = sz_configmanager.register_config(config_definition, config_comment)
except SzError as err:
    print(f"\nERROR: {err}\n")
