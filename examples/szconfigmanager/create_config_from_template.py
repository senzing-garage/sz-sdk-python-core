from senzing import SzError

from . import sz_configmanager

try:
    sz_config = sz_configmanager.create_config_from_template()
except SzError as err:
    print(f"\nERROR: {err}\n")
