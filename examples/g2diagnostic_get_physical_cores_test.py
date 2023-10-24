from senzing import g2diagnostic

ENGINE_CONFIGURATION_JSON = '{"PIPELINE":{"CONFIGPATH":"/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/g2/resources","SUPPORTPATH":"/opt/senzing/data"},"SQL":{"CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db"}}'
G2_DIAGNOSTIC = g2diagnostic.G2Diagnostic("Example", ENGINE_CONFIGURATION_JSON, 0)
NUMBER_OF_PHYSICAL_CORES = G2_DIAGNOSTIC.get_physical_cores()
print(NUMBER_OF_PHYSICAL_CORES)
