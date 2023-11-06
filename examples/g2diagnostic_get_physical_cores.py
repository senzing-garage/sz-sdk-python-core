from senzing import g2diagnostic

INI_PARAMS = '{"PIPELINE":{"CONFIGPATH":"/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/g2/resources","SUPPORTPATH":"/opt/senzing/data"},"SQL":{"CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db"}}'
G2_DIAGNOSTIC = g2diagnostic.G2Diagnostic("Example", INI_PARAMS, 0)
NUMBER_OF_PHYSICAL_CORES = G2_DIAGNOSTIC.get_physical_cores()
print(NUMBER_OF_PHYSICAL_CORES)
