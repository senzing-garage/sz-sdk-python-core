import json
import platform
from typing import Any, Dict

import pytest


@pytest.fixture(name="engine_vars", scope="session")
def engine_vars_fixture() -> Dict[Any, Any]:
    """Return a dictionary of Senzing engine variables based on runtime env
    Can be used by all pytest tests.
    """

    result = {"INSTANCE_NAME": "Testing", "VERBOSE_LOGGING": 0}

    linux_config = {
        "PIPELINE": {
            "CONFIGPATH": "/etc/opt/senzing",
            "RESOURCEPATH": "/opt/senzing/er/resources",
            "SUPPORTPATH": "/opt/senzing/data",
        },
        "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
    }

    darwin_config = {
        "PIPELINE": {
            "CONFIGPATH": "/opt/senzing/er/etc",
            "RESOURCEPATH": "/opt/senzing/er/resources",
            "SUPPORTPATH": "/opt/senzing/data",
        },
        "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
    }

    windows_config = {
        "PIPELINE": {
            "CONFIGPATH": "C:\\Program Files\\Senzing\\er\\etc",
            "RESOURCEPATH": "C:\\Program Files\\Senzing\\er\\resources",
            "SUPPORTPATH": "C:\\Program Files\\Senzing\\data",
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
