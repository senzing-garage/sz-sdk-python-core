#! /usr/bin/env python3
import json
import sys
import time
from contextlib import suppress
from datetime import timedelta

from senzing.szexception import SzException

from senzing import szengine, szengineflags

with suppress(ModuleNotFoundError):
    import orjson

INSTANCE_NAME = "Example"
ENTITY_ID = 1
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}

try:
    sz_engine = szengine.SzEngine(INSTANCE_NAME, SETTINGS)
except SzException as err:
    print(err)
    sys.exit()

flags = szengineflags.G2EngineFlags.G2_ENTITY_BRIEF_DEFAULT_FLAGS
iterations = 5


starttime = time.perf_counter()
for _ in range(iterations):
    result = sz_engine.get_entity_by_entity_id(ENTITY_ID, flags)
    json.loads(result)
duration = timedelta(seconds=time.perf_counter() - starttime)
print(f"json duration: {duration}")

if "orjson" in dir():
    starttime = time.perf_counter()
    for _ in range(iterations):
        result = sz_engine.get_entity_by_entity_id(ENTITY_ID, flags)
        orjson.loads(result)
    duration = timedelta(seconds=time.perf_counter() - starttime)
    print(f"orjson duration: {duration}")
