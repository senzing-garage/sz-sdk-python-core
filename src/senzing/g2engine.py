#! /usr/bin/env python3

"""
TODO: g2engine.py
"""

# Import from standard library. https://docs.python.org/3/library/

from typing import Tuple
# from ctypes import *
# import functools
# import json
# import os
# import threading
# import warnings

# Import from https://pypi.org/

# Import from Senzing.

# from .g2exception import translate_exception
# from .g2engineflags import G2EngineFlags

from .g2engine_abstract import G2EngineAbstract


# Metadata

__all__ = ['G2Engine']
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2023-10-30'
__updated__ = '2023-10-30'

SENZING_PRODUCT_ID = "5043"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md

# -----------------------------------------------------------------------------
# G2Engine class
# -----------------------------------------------------------------------------


class G2Engine(G2EngineAbstract):
    """
    G2 engine module access library
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(self, module_name, ini_params, verbose_logging, *args, **kwargs) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """

        self.ini_params = ini_params
        self.module_name = module_name
        self.noop = ""
        self.verbose_logging = verbose_logging

        self.init(self.module_name, self.ini_params, self.verbose_logging)

    def __del__(self):
        """Destructor"""
        self.destroy()

    # -------------------------------------------------------------------------
    # Development methods - to be removed after initial development
    # -------------------------------------------------------------------------

    def fake_g2engine(self, *args, **kwargs):
        """TODO: Remove once SDK methods have been implemented."""
        if len(args) + len(kwargs) > 2000:
            print(self.noop)

    # -------------------------------------------------------------------------
    # G2Engine methods
    # -------------------------------------------------------------------------

    def add_record(self, data_source_code: str, record_id: str, json_data: str, load_id: str, *args, **kwargs) -> None:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id, json_data, load_id)

    def add_record_with_info(self, data_source_code: str, record_id: str, json_data: str, load_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id, json_data, load_id, flags)
        return "string"

    def close_export(self, response_handle: int, *args, **kwargs) -> None:
        """TODO: document"""
        self.fake_g2engine(response_handle)

    def count_redo_records(self, *args, **kwargs) -> int:
        """TODO: document"""
        self.fake_g2engine()
        return "int64"

    def delete_record(self, data_source_code: str, record_id: str, load_id: str, *args, **kwargs) -> None:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id, load_id)

    def delete_record_with_info(self, data_source_code: str, record_id: str, load_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id, load_id, flags)
        return "string"

    def destroy(self, *args, **kwargs) -> None:
        """TODO: document"""
        self.fake_g2engine()

    def export_config(self, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine()
        return "string"

    def export_config_and_config_id(self, *args, **kwargs) -> Tuple[str, int]:
        """TODO: document"""
        self.fake_g2engine()
        return "string", "int64"

    def export_csv_entity_report(self, csv_column_list: str, flags: int, *args, **kwargs) -> int:
        """TODO: document"""
        self.fake_g2engine(csv_column_list, flags)
        return "uintptr"

    def export_json_entity_report(self, flags: int, *args, **kwargs) -> int:
        """TODO: document"""
        self.fake_g2engine(flags)
        return "uintptr"

    def fetch_next(self, response_handle: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(response_handle)
        return "string"

    def find_interesting_entities_by_entity_id(self, entity_id: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id, flags)
        return "string"

    def find_interesting_entities_by_record_id(self, data_source_code: str, record_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def find_network_by_entity_id_v2(self, entity_list: str, max_degree: int, build_out_degree: int, max_entities: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_list, max_degree, build_out_degree, max_entities, flags)
        return "string"

    def find_network_by_entity_id(self, entity_list: str, max_degree: int, build_out_degree: int, max_entities: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_list, max_degree, build_out_degree, max_entities)
        return "string"

    def find_network_by_record_id_v2(self, record_list: str, max_degree: int, build_out_degree: int, max_entities: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(record_list, max_degree, build_out_degree, max_entities, flags)
        return "string"

    def find_network_by_record_id(self, record_list: str, max_degree: int, build_out_degree: int, max_entities: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(record_list, max_degree, build_out_degree, max_entities)
        return "string"

    def find_path_by_entity_id_v2(self, entity_id_1: int, entity_id_2: int, max_degree: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id_1, entity_id_2, max_degree, flags)
        return "string"

    def find_path_by_entity_id(self, entity_id_1: int, entity_id_2: int, max_degree: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id_1, entity_id_2, max_degree)
        return "string"

    def find_path_by_record_id_v2(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, max_degree: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code_1, record_id_1, data_source_code_2, record_id_2, max_degree, flags)
        return "string"

    def find_path_by_record_id(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, max_degree: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code_1, record_id_1, data_source_code_2, record_id_2, max_degree)
        return "string"

    def find_path_excluding_by_entity_id_v2(self, entity_id_1: int, entity_id_2: int, max_degree: int, excluded_entities: str, flags: str, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id_1, entity_id_2, max_degree, excluded_entities, flags)
        return "string"

    def find_path_excluding_by_entity_id(self, entity_id_1: int, entity_id_2: int, max_degree: int, excluded_entities: str, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id_1, entity_id_2, max_degree, excluded_entities)
        return "string"

    def find_path_excluding_by_record_id_v2(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, max_degree: int, excluded_records: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code_1, record_id_1, data_source_code_2, record_id_2, max_degree, excluded_records, flags)
        return "string"

    def find_path_excluding_by_record_id(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, max_degree: int, excluded_records: str, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code_1, record_id_1, data_source_code_2, record_id_2, max_degree, excluded_records)
        return "string"

    def find_path_including_source_by_entity_id_v2(self, entity_id_1: int, entity_id_2: int, max_degree: int, excluded_entities: str, required_dsrcs: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id_1, entity_id_2, max_degree, excluded_entities, required_dsrcs, flags)
        return "string"

    def find_path_including_source_by_entity_id(self, entity_id_1: int, entity_id_2: int, max_degree: int, excluded_entities: str, required_dsrcs: str, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id_1, entity_id_2, max_degree, excluded_entities, required_dsrcs)
        return "string"

    def find_path_including_source_by_record_id_v2(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, max_degree: int, excluded_records: str, required_dsrcs: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code_1, record_id_1, data_source_code_2, record_id_2, max_degree, excluded_records, required_dsrcs, flags)
        return "string"

    def find_path_including_source_by_record_id(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, max_degree: int, excluded_records: str, required_dsrcs: str, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code_1, record_id_1, data_source_code_2, record_id_2, max_degree, excluded_records, required_dsrcs)
        return "string"

    def get_active_config_id(self, *args, **kwargs) -> int:
        """TODO: document"""
        self.fake_g2engine()
        return "int64"

    def get_entity_by_entity_id_v2(self, entity_id: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id, flags)
        return "string"

    def get_entity_by_entity_id(self, entity_id: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id)
        return "string"

    def get_entity_by_record_id_v2(self, data_source_code: str, record_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def get_entity_by_record_id(self, data_source_code: str, record_id: str, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id)
        return "string"

    def get_record_v2(self, data_source_code: str, record_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def get_record(self, data_source_code: str, record_id: str, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id)
        return "string"

    def get_redo_record(self, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine()
        return "string"

    def get_repository_last_modified_time(self, *args, **kwargs) -> int:
        """TODO: document"""
        self.fake_g2engine()
        return "int64"

    def get_virtual_entity_by_record_id_v2(self, record_list: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(record_list, flags)
        return "string"

    def get_virtual_entity_by_record_id(self, record_list: str, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(record_list)
        return "string"

    def how_entity_by_entity_id_v2(self, entity_id: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id, flags)
        return "string"

    def how_entity_by_entity_id(self, entity_id: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id)
        return "string"

    def init(self, module_name: str, ini_params: str, verbose_logging: int, *args, **kwargs) -> None:
        """TODO: document"""
        self.fake_g2engine(module_name, ini_params, verbose_logging)

    def init_with_config_id(self, module_name: str, ini_params: str, init_config_id: int, verbose_logging: int, *args, **kwargs) -> None:
        """TODO: document"""
        self.fake_g2engine(module_name, ini_params, init_config_id, verbose_logging)

    def prime_engine(self, *args, **kwargs) -> None:
        """TODO: document"""
        self.fake_g2engine()

    def process(self, record: str, *args, **kwargs) -> None:
        """TODO: document"""
        self.fake_g2engine(record)

    def process_with_info(self, record: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(record, flags)
        return "string"

    def purge_repository(self, *args, **kwargs) -> None:
        """TODO: document"""
        self.fake_g2engine()

    def reevaluate_entity(self, entity_id: int, flags: int, *args, **kwargs) -> None:
        """TODO: document"""
        self.fake_g2engine(entity_id, flags)

    def reevaluate_entity_with_info(self, entity_id: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id, flags)
        return "string"

    def reevaluate_record(self, data_source_code: str, record_id: str, flags: int, *args, **kwargs) -> None:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id, flags)

    def reevaluate_record_with_info(self, data_source_code: str, record_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def reinit(self, init_config_id: int, *args, **kwargs) -> None:
        """TODO: document"""
        self.fake_g2engine(init_config_id)

    def replace_record(self, data_source_code: str, record_id: str, json_data: str, load_id: str, *args, **kwargs) -> None:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id, json_data, load_id)

    def replace_record_with_info(self, data_source_code: str, record_id: str, json_data: str, load_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id, json_data, load_id, flags)
        return "string"

    def search_by_attributes_v2(self, json_data: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(json_data, flags)
        return "string"

    def search_by_attributes(self, json_data: str, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(json_data)
        return "string"

    def stats(self, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine()
        return "string"

    def why_entities_v2(self, entity_id_1: int, entity_id_2: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id_1, entity_id_2, flags)
        return "string"

    def why_entities(self, entity_id_1: int, entity_id_2: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id_1, entity_id_2)
        return "string"

    def why_entity_by_entity_id_v2(self, entity_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id, flags)
        return "string"

    def why_entity_by_entity_id(self, entity_id: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(entity_id)
        return "string"

    def why_entity_by_record_id_v2(self, data_source_code: str, record_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def why_entity_by_record_id(self, data_source_code: str, record_id: str, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code, record_id)
        return "string"

    def why_records_v2(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code_1, record_id_1, data_source_code_2, record_id_2, flags)
        return "string"

    def why_records(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, *args, **kwargs) -> str:
        """TODO: document"""
        self.fake_g2engine(data_source_code_1, record_id_1, data_source_code_2, record_id_2)
        return "string"
