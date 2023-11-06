from senzing import g2configmgr
from senzing.g2exception import G2Exception

ENGINE_CONFIGURATION_JSON = '{"PIPELINE":{"CONFIGPATH":"/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/g2/resources","SUPPORTPATH":"/opt/senzing/data"},"SQL":{"CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db"}}'
ENGINE_MODULE_NAME = "EXAMPLE"
ENGINE_VERBOSE_LOGGING = 0

try:
    G2_CONFIGMGR = g2configmgr.G2ConfigMgr(
        ENGINE_MODULE_NAME, ENGINE_CONFIGURATION_JSON, ENGINE_VERBOSE_LOGGING
    )
    config_id = G2_CONFIGMGR.get_default_config_id()
    print(config_id)
except G2Exception as err:
    print(err)
