import json

# import platform
from sys import platform

import pytest

# Ant test
# '{"PIPELINE": {"SUPPORTPATH": "/home/ant/senzprojs/3.8.0.23292/data", "CONFIGPATH": "/home/ant/senzprojs/3.8.0.23292/etc", "RESOURCEPATH": "/home/ant/senzprojs/3.8.0.23292/resources"}, "SQL": {"CONNECTION": "postgresql://senzing:password@ant76:5432:g2"}}'


# @pytest.fixture(scope="session")
# def engine_vars():
#    """_summary_"""
# eng_vars = {"ENGINE_MODULE_NAME": "Testing", "ENGINE_VERBOSE_LOGGING": 0}
# linux_json = '{"PIPELINE":{"CONFIGPATH":"/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/g2/resources","SUPPORTPATH":"/opt/senzing/data"},"SQL":{"CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db"}}'
# # ANT linux_json = '{"PIPELINE": {"SUPPORTPATH": "/home/ant/senzprojs/3.8.0.23292/data", "CONFIGPATH": "/home/ant/senzprojs/3.8.0.23292/etc", "RESOURCEPATH": "/home/ant/senzprojs/3.8.0.23292/resources"}, "SQL": {"CONNECTION": "postgresql://senzing:password@ant76:5432:g2"}}'
# darwin_json = r'{"PIPELINE":{"CONFIGPATH":"/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/g2/resources","SUPPORTPATH":"/opt/senzing/g2/data"},"SQL":{"CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db"}}'
# windows_json = '{"PIPELINE":{"CONFIGPATH":"C:/Program Files/Senzing/g2","RESOURCEPATH":"C:/Program Files/Senzing/g2/resources","SUPPORTPATH":"C:/Program Files/Senzing/g2/data"},"SQL":{"CONNECTION":"sqlite3://na:na@C:/Temp/sqlite/G2C.db"}}'


#
# os = platform.system()
#
# if os == "Linux":
#     eng_vars["ENGINE_CONFIGURATION_JSON"] = linux_json
#
# if os == "Darwin":
#     eng_vars["ENGINE_CONFIGURATION_JSON"] = darwin_json
#
# if os == "Windows":
#     eng_vars["ENGINE_CONFIGURATION_JSON"] = windows_json
#
# # Debug
# print(os)
# print()
# print(eng_vars["ENGINE_CONFIGURATION_JSON"])
# print()
#
# return eng_vars


# def get_test_engine_configuration_json() -> str:
@pytest.fixture(scope="session")
def engine_vars():
    """Get a platform-specific version of the Senzing engine configuration JSON"""
    if platform in ("linux" "linux2"):
        test_engine_configuration = {
            "PIPELINE": {
                "CONFIGPATH": "/etc/opt/senzing",
                "RESOURCEPATH": "/opt/senzing/g2/resources",
                "SUPPORTPATH": "/opt/senzing/data",
            },
            "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
        }
    elif platform == "darwin":
        test_engine_configuration = {
            "PIPELINE": {
                "CONFIGPATH": "/opt/senzing/g2/etc",
                "RESOURCEPATH": "/opt/senzing/g2/resources",
                "SUPPORTPATH": "/opt/senzing/g2/data",
            },
            "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
        }
    elif platform == "win32":
        test_engine_configuration = {
            "PIPELINE": {
                "CONFIGPATH": "C:\\Program Files\\Senzing\\g2\\etc",
                "RESOURCEPATH": "C:\\Program Files\\Senzing\\g2\\resources",
                "SUPPORTPATH": "C:\\Program Files\\Senzing\\g2\\data",
            },
            "SQL": {"CONNECTION": "sqlite3://na:na@nowhere/C:\\Temp\\sqlite\\G2C.db"},
        }
    else:
        test_engine_configuration = {}

    eng_vars = {"ENGINE_MODULE_NAME": "Testing", "ENGINE_VERBOSE_LOGGING": 0}
    eng_vars["ENGINE_CONFIGURATION_JSON"] = json.dumps(test_engine_configuration)

    # # Debug
    print(platform)
    print()
    print(eng_vars["ENGINE_CONFIGURATION_JSON"])
    print()

    # return json.dumps(test_engine_configuration)
    return eng_vars
