#! /usr/bin/env python3

from senzing import (
    SzAbstractFactory,
    SzAbstractFactoryParameters,
    SzEngineFlags,
    SzError,
)

ENTITY_ID_1 = 1
ENTITY_ID_2 = 4
FACTORY_PARAMETERS: SzAbstractFactoryParameters = {
    "instance_name": "Example",
    "settings": {
        "PIPELINE": {
            "CONFIGPATH": "/etc/opt/senzing",
            "RESOURCEPATH": "/opt/senzing/er/resources",
            "SUPPORTPATH": "/opt/senzing/data",
        },
        "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
    },
}
FLAGS = SzEngineFlags.SZ_WHY_ENTITIES_DEFAULT_FLAGS

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
    sz_engine = sz_abstract_factory.create_sz_engine()
    RESULT = sz_engine.why_entities(
        ENTITY_ID_1,
        ENTITY_ID_2,
        FLAGS,
    )
    print(RESULT)
except SzError as err:
    print(f"\nError in {__file__}: {err}\n")
