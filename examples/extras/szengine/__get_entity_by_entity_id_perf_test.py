#! /usr/bin/env python3
# TODO: Create testable example.
# import json
# import sys
# import time
# from contextlib import suppress
# from datetime import timedelta

# from senzing import SzEngineFlags, SzError, szengine

# with suppress(ModuleNotFoundError):
#     import orjson

# INSTANCE_NAME = "Example"
# ENTITY_ID = 1
# SETTINGS = {
#     "PIPELINE": {
#         "CONFIGPATH": "/etc/opt/senzing",
#         "RESOURCEPATH": "/opt/senzing/er/resources",
#         "SUPPORTPATH": "/opt/senzing/data",
#     },
#     "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
# }

# try:
#     sz_engine = SzEngine(INSTANCE_NAME, SETTINGS)
# except SzError as err:
#     print(f"\nError in {__file__}: {err}\n")

#     sys.exit()

# flags = SzEngineFlags.SZ_ENTITY_BRIEF_DEFAULT_FLAGS
# iterations = 5


# starttime = time.perf_counter()
# for _ in range(iterations):
#     result = sz_engine.get_entity_by_entity_id(ENTITY_ID, flags)
#     json.loads(result)
# duration = timedelta(seconds=time.perf_counter() - starttime)
# print(f"json duration: {duration}")

# if "orjson" in dir():
#     starttime = time.perf_counter()
#     for _ in range(iterations):
#         result = sz_engine.get_entity_by_entity_id(ENTITY_ID, flags)
#         orjson.loads(result)
#     duration = timedelta(seconds=time.perf_counter() - starttime)
#     print(f"orjson duration: {duration}")
