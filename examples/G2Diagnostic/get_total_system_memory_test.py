from senzing import g2diagnostic
from senzing.g2exception import G2Exception

# ENGINE_CONFIGURATION_JSON = '{"PIPELINE":{"CONFIGPATH":"/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/g2/resources","SUPPORTPATH":"/opt/senzing/data"},"SQL":{"CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db"}}'
ENGINE_MODULE_NAME = "EXAMPLE"
ENGINE_CONFIGURATION_JSON = '{"PIPELINE": {"CONFIGPATH": "/home/ant/senzprojs/3.8.0.23292/etc", "RESOURCEPATH": "/home/ant/senzprojs/3.8.0.23292/resources", "SUPPORTPATH": "/home/ant/senzprojs/3.8.0.23292/data"}, "SQL": {"CONNECTION": "postgresql://senzing:password@ant76:5432:g2"}}'
ENGINE_VERBOSE_LOGGING = 0

try:
    G2_DIAGNOSTIC = g2diagnostic.G2Diagnostic(
        ENGINE_MODULE_NAME, ENGINE_CONFIGURATION_JSON, ENGINE_VERBOSE_LOGGING
    )
except G2Exception as err:
    print(err)
else:
    total_mem = G2_DIAGNOSTIC.get_total_system_memory()
    total_mem_gb = f"{total_mem / (1024 * 1024 * 1024):.1f} GB"
    print(total_mem_gb)
