import json
import platform

import pytest

# Ant test
# '{"PIPELINE": {"SUPPORTPATH": "/home/ant/senzprojs/3.8.0.23292/data", "CONFIGPATH": "/home/ant/senzprojs/3.8.0.23292/etc", "RESOURCEPATH": "/home/ant/senzprojs/3.8.0.23292/resources"}, "SQL": {"CONNECTION": "postgresql://senzing:password@ant76:5432:g2"}}'


@pytest.fixture(name="engine_vars", scope="session")
def engine_vars_fixture():
    """Return a dictionary of Senzing engine variables based on runtime env
    Can be used by all pytest tests.
    """

    result = {"INSTANCE_NAME": "Testing", "VERBOSE_LOGGING": 0}

    linux_config = {
        "PIPELINE": {
            "CONFIGPATH": "/etc/opt/senzing",
            "RESOURCEPATH": "/opt/senzing/g2/resources",
            "SUPPORTPATH": "/opt/senzing/data",
        },
        "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
    }

    darwin_config = {
        "PIPELINE": {
            "CONFIGPATH": "/opt/senzing/g2/etc",
            "RESOURCEPATH": "/opt/senzing/g2/resources",
            "SUPPORTPATH": "/opt/senzing/g2/data",
        },
        "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
    }

    windows_config = {
        "PIPELINE": {
            "CONFIGPATH": "C:\\Program Files\\Senzing\\g2\\etc",
            "RESOURCEPATH": "C:\\Program Files\\Senzing\\g2\\resources",
            "SUPPORTPATH": "C:\\Program Files\\Senzing\\g2\\data",
        },
        "SQL": {"CONNECTION": "sqlite3://na:na@nowhere/C:\\Temp\\sqlite\\G2C.db"},
    }

    run_platform = platform.system()

    if run_platform == "Linux":
        result["SETTINGS"] = json.dumps(linux_config)
        result["SETTINGS_DICT"] = linux_config
    elif run_platform == "Darwin":
        result["SETTINGS"] = json.dumps(darwin_config)
        result["SETTINGS_DICT"] = darwin_config
    elif run_platform == "Windows":
        result["SETTINGS"] = json.dumps(windows_config)
        result["SETTINGS_DICT"] = windows_config
    else:
        result["SETTINGS"] = json.dumps({})
        result["SETTINGS_DICT"] = {}

    return result
