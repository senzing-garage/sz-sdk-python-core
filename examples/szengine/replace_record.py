#! /usr/bin/env python3

from senzing import szengine
from senzing.szexception import SzException

DATA_SOURCE_CODE = "TEST"
INSTANCE_NAME = "Example"
RECORD_DEFINITION = {
    "RECORD_DEFINITION_TYPE": "PERSON",
    "PRIMARY_NAME_LAST": "Smith",
    "PRIMARY_NAME_FIRST": "Robert",
    "DATE_OF_BIRTH": "12/11/1978",
    "ADDR_TYPE": "MAILING",
    "ADDR_LINE1": "123 Main Street, Las Vegas NV 89132",
    "PHONE_TYPE": "HOME",
    "PHONE_NUMBER": "787-208-7676",
    "EMAIL_ADDRESS": "bsmith@home.com",
    "DATE": "1/2/18",
    "STATUS": "Active",
    "AMOUNT": "100",
}
RECORD_ID = "Example-1"
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
    sz_engine.replace_record(DATA_SOURCE_CODE, RECORD_ID, RECORD_DEFINITION)
except SzException as err:
    print(err)
