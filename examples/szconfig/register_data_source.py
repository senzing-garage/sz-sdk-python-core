from senzing import SzError

from senzing_core import SzAbstractFactoryCore

data_source_code = "NAME_OF_DATASOURCE"
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
    result = sz_config.register_data_source(data_source_code)
    print(f"\n{result}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
