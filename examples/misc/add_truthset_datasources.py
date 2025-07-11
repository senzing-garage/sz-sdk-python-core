from senzing import SzError
from senzing_truthset import TRUTHSET_DATASOURCES

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
    sz_configmanager = sz_abstract_factory.create_configmanager()
    sz_config = sz_configmanager.create_config_from_template()

    # Create a new Senzing configuration with additional datasources.

    current_default_config_id = sz_configmanager.get_default_config_id()
    sz_config = sz_configmanager.create_config_from_config_id(current_default_config_id)
    for data_source_code in TRUTHSET_DATASOURCES:
        sz_config.register_data_source(data_source_code)

    # Persist new Senzing configuration.

    new_config_definition = sz_config.export()
    new_default_config_id = sz_configmanager.register_config(new_config_definition, "Add TruthSet datasources")

    # Make new Senzing configuration the default and the active configuration.

    sz_configmanager.replace_default_config_id(current_default_config_id, new_default_config_id)
    sz_abstract_factory.reinitialize(new_default_config_id)
except SzError as err:
    print(f"\nERROR: {err}\n")
