from senzing import SzError

from . import sz_configmanager

try:
    CONFIG_COMMENT = "Just an empty example"
    sz_config = sz_configmanager.create_config_from_template()
    CONFIG_DEFINITION = sz_config.export()
    CONFIG_ID = sz_configmanager.register_config(CONFIG_DEFINITION, CONFIG_COMMENT)
except SzError as err:
    print(f"\nERROR: {err}\n")
