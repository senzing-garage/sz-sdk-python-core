from senzing import SzError

from . import sz_configmanager

try:
    CONFIG_ID = sz_configmanager.get_default_config_id()
    sz_config = sz_configmanager.create_config_from_config_id(CONFIG_ID)
except SzError as err:
    print(f"\nERROR: {err}\n")
