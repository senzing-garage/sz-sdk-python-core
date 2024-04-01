#! /usr/bin/env python3

from senzing import g2engine
from senzing.g2exception import G2Exception

DATA_SOURCE_CODE = "TEST"
SETTINGS = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/g2/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/var/opt/senzing/G2C.db"},
}
INSTANCE_NAME = "Example"
RECORD_DEFINITION = {
    "RECORD_DEFINITION_TYPE": "PERSON",
    "PRIMARY_NAME_LAST": "Smith",
    "PRIMARY_NAME_FIRST": "Robert",
    "DATE_OF_BIRTH": "12/11/1978",
    "ADDR_TYPE": "MAILING",
    """ """ """ """ "ADDR_LINE1": "123 Main Street, Las Vegas NV 89132",
    "PHONE_TYPE": "HOME",
    "PHONE_NUMBER": "702-919-1300",
    "EMAIL_ADDRESS": "bsmith@work.com",
    "DATE": "1/2/18",
    "STATUS": "Active",
    "AMOUNT": "100",
}
RECORD_ID = "Example-1"

try:
    g2_engine = g2engine.G2Engine(INSTANCE_NAME, SETTINGS)
    result = g2_engine.add_record_return_dict(DATA_SOURCE_CODE, RECORD_ID, RECORD_DEFINITION, 1)
    print(result)
except G2Exception as err:
    print(err)
