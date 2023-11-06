from senzing import g2diagnostic
from senzing.g2exception import G2Exception

ENGINE_CONFIGURATION_JSON = '{"PIPELINE":{"CONFIGPATH":"/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/g2/resources","SUPPORTPATH":"/opt/senzing/data"},"SQL":{"CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db"}}'
ENGINE_MODULE_NAME = "EXAMPLE"
ENGINE_VERBOSE_LOGGING = 0

try:
    G2_DIAGNOSTIC = g2diagnostic.G2Diagnostic(
        ENGINE_MODULE_NAME, ENGINE_CONFIGURATION_JSON, ENGINE_VERBOSE_LOGGING
    )
except G2Exception as err:
    print(err)
else:
    physical_cores = G2_DIAGNOSTIC.get_physical_cores()
    print(physical_cores)
