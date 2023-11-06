import json
import platform

import pytest

# Ant test
# '{"PIPELINE": {"SUPPORTPATH": "/home/ant/senzprojs/3.8.0.23292/data", "CONFIGPATH": "/home/ant/senzprojs/3.8.0.23292/etc", "RESOURCEPATH": "/home/ant/senzprojs/3.8.0.23292/resources"}, "SQL": {"CONNECTION": "postgresql://senzing:password@ant76:5432:g2"}}'


@pytest.fixture(scope="session")
def build_engine_vars():
    """Return a dictionary of Senzing engine variables based on runtime env
    Can be used by all pytest tests.
    """

    engine_vars = {"ENGINE_MODULE_NAME": "Testing", "ENGINE_VERBOSE_LOGGING": 0}

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
        engine_vars["ENGINE_CONFIGURATION_JSON"] = json.dumps(linux_config)
    elif run_platform == "Darwin":
        engine_vars["ENGINE_CONFIGURATION_JSON"] = json.dumps(darwin_config)
    elif run_platform == "Windows":
        engine_vars["ENGINE_CONFIGURATION_JSON"] = json.dumps(windows_config)
    else:
        engine_vars["ENGINE_CONFIGURATION_JSON"] = json.dumps({})

    return engine_vars
