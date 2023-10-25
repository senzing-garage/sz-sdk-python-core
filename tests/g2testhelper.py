"""
# -----------------------------------------------------------------------------
# g2testhelper.py
# -----------------------------------------------------------------------------
"""

import json
from sys import platform


def get_test_engine_configuration_json() -> str:
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

    return json.dumps(test_engine_configuration)
