import json

from senzing import SzError

from . import sz_configmanager

try:
    CONFIG_DEFINITION = json.dumps({})
    sz_config = sz_configmanager.create_config_from_string(CONFIG_DEFINITION)
except SzError as err:
    print(f"\nERROR: {err}\n")
