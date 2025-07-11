import time

from senzing import SzError

from senzing_core import SzAbstractFactoryCore

config_comment = "Just an example"
data_source_code = f"REPLACE_DEFAULT_CONFIG_ID_{time.time()}"
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

    # Create a new config.

    sz_config = sz_configmanager.create_config_from_template()
    sz_config.register_data_source(data_source_code)

    # Persist the new default config.

    config_definition = sz_config.export()
    config_id = sz_configmanager.set_default_config(config_definition, config_comment)
    print(config_id)
except SzError as err:
    print(f"\nERROR: {err}\n")
