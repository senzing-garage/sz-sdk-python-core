import json

from senzing import SzEngineFlags, SzError

from senzing_core import SzAbstractFactoryCore

instance_name = "Example"
# TODO - Change when new default is in V4
flags = SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS
record_definition = json.dumps(
    {
        "RECORD_TYPE": "PERSON",
        "NAME_TYPE": "PRIMARY",
        "NAME_LAST": "Smith",
        "NAME_FIRST": "Robert",
        "DATE_OF_BIRTH": "12/11/1978",
        "ADDR_TYPE": "MAILING",
        "ADDR_FULL": "123 Main Street, Las Vegas NV 89132",
        "PHONE_TYPE": "HOME",
        "PHONE_NUMBER": "702-919-1300",
        "EMAIL_ADDRESS": "bsmith@work.com",
        "DATE": "1/2/18",
        "STATUS": "Active",
        "AMOUNT": "100",
    }
)
settings = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/er/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}

try:
    sz_abstract_factory = SzAbstractFactoryCore(instance_name, settings)
    sz_engine = sz_abstract_factory.create_engine()
    result = sz_engine.preprocess_record(record_definition, flags)
    print(f"\n{result}\n")
except SzError as err:
    print(f"\nERROR: {err}\n")
