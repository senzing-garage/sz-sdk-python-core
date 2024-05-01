#! /usr/bin/env python3

import grpc
from senzing_truthset import TRUTHSET_DATASOURCES

from senzing_grpc import (
    SzConfigGrpc,
    SzConfigManagerGrpc,
    SzDiagnosticGrpc,
    SzEngineGrpc,
    SzError,
)

GRPC_URL = "localhost:8261"

try:
    grpc_channel = grpc.insecure_channel(GRPC_URL)
    sz_config = SzConfigGrpc(grpc_channel=grpc_channel)
    sz_configmgr = SzConfigManagerGrpc(grpc_channel=grpc_channel)
    current_default_config_id = sz_configmgr.get_default_config_id()
    OLD_CONFIG_DEFINITION = sz_configmgr.get_config(current_default_config_id)
    config_handle = sz_config.import_config(OLD_CONFIG_DEFINITION)
    for data_source_code in TRUTHSET_DATASOURCES.keys():
        sz_config.add_data_source(config_handle, data_source_code)
    NEW_CONFIG_DEFINITION = sz_config.export_config(config_handle)
    new_default_config_id = sz_configmgr.add_config(
        NEW_CONFIG_DEFINITION, "Add TruthSet datasources"
    )
    sz_configmgr.replace_default_config_id(
        current_default_config_id, new_default_config_id
    )
    sz_engine = SzEngineGrpc(grpc_channel=grpc_channel)
    sz_engine.reinitialize(new_default_config_id)
    sz_diagnostic = SzDiagnosticGrpc(grpc_channel=grpc_channel)
    sz_diagnostic.reinitialize(new_default_config_id)
except SzError as err:
    print(f"\nError:\n{err}\n")
