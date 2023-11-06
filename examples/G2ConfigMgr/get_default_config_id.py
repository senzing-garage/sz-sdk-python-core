from senzing import g2configmgr
from senzing.g2exception import G2Exception

# ENGINE_CONFIGURATION_JSON = '{"PIPELINE":{"CONFIGPATH":"/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/g2/resources","SUPPORTPATH":"/opt/senzing/data"},"SQL":{"CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db"}}'
ENGINE_MODULE_NAME = "EXAMPLE"
ENGINE_CONFIGURATION_JSON = '{"PIPELINE": {"CONFIGPATH": "/home/ant/senzprojs/3.8.0.23292/etc", "RESOURCEPATH": "/home/ant/senzprojs/3.8.0.23292/resources", "SUPPORTPATH": "/home/ant/senzprojs/3.8.0.23292/data"}, "SQL": {"CONNECTION": "postgresql://senzing:password@ant76:5432:g2"}}'
ENGINE_VERBOSE_LOGGING = 0

try:
    G2_CONFIGMGR = g2configmgr.G2ConfigMgr(
        ENGINE_MODULE_NAME, ENGINE_CONFIGURATION_JSON, ENGINE_VERBOSE_LOGGING
    )
    config_id = G2_CONFIGMGR.get_default_config_id()
    print(config_id)
except G2Exception as err:
    print(err)
