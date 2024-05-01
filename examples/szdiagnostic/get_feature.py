#! /usr/bin/env python3

# TODO: Create a testable example

# from senzing import SzError, SzDiagnostic

# INSTANCE_NAME = "Example"
# SETTINGS = {
#     "PIPELINE": {
#         "CONFIGPATH": "/etc/opt/senzing",
#         "RESOURCEPATH": "/opt/senzing/g2/resources",
#         "SUPPORTPATH": "/opt/senzing/data",
#     },
#     "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
# }

# try:
#     sz_diagnostic = SzDiagnostic(INSTANCE_NAME, SETTINGS)
#     result = sz_diagnostic.get_feature(1)
#     print(result)
# except SzError as err:
#     print(f"\nError:\n{err}\n")
