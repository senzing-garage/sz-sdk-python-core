#! /usr/bin/env python3

from senzing_core import (
    SzAbstractFactory,
    SzAbstractFactoryParameters,
    SzEngineFlags,
    SzError,
)

DATA_SOURCE_CODE = "TEST"
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
FLAGS = SzEngineFlags.SZ_WITH_INFO
RECORD_DEFINITION = (
    "{"
    '"RECORD_TYPE": "PERSON",'
    '"PRIMARY_NAME_LAST": "Smith",'
    '"PRIMARY_NAME_FIRST": "Robert",'
    '"DATE_OF_BIRTH": "12/11/1978",'
    '"ADDR_TYPE": "MAILING",'
    '"ADDR_LINE1": "123 Main Street, Las Vegas NV 89132",'
    '"PHONE_TYPE": "HOME",'
    '"PHONE_NUMBER": "702-919-1300",'
    '"EMAIL_ADDRESS": "bsmith@work.com",'
    '"DATE": "1/2/18",'
    '"STATUS": "Active",'
    '"AMOUNT": "100"'
    "}"
)
RECORD_ID = "1"

try:
    sz_abstract_factory = SzAbstractFactory(**FACTORY_PARAMETERS)
    sz_engine = sz_abstract_factory.create_engine()
    RESULT = sz_engine.add_record(DATA_SOURCE_CODE, RECORD_ID, RECORD_DEFINITION, FLAGS)
    print(f"\nFile {__file__}:\n{RESULT}\n")
except SzError as err:
    print(f"\nFile {__file__}:\nError:\n{err}\n")
