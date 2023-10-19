#! /usr/bin/env python3

"""
TODO: g2engine_abstract.py
"""

# Import from standard library. https://docs.python.org/3/library/

import json
from abc import ABC, abstractmethod
from typing import Tuple

# Metadata

__all__ = ['G2EngineAbstract']
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2023-10-30'
__updated__ = '2023-10-30'


class G2EngineAbstract(ABC):
    """
    G2 diagnostic module access library
    """

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def add_record(self, data_source_code: str, record_id: str, json_data: str, load_id: str, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def add_record_with_info(self, data_source_code: str, record_id: str, json_data: str, load_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def close_export(self, response_handle: int, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def count_redo_records(self, *args, **kwargs) -> int:
        """TODO: document"""

    @abstractmethod
    def delete_record(self, data_source_code: str, record_id: str, load_id: str, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def delete_record_with_info(self, data_source_code: str, record_id: str, load_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def destroy(self, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def export_config(self, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def export_config_and_config_id(self, *args, **kwargs) -> Tuple[str, int]:
        """TODO: document"""

    @abstractmethod
    def export_csv_entity_report(self, csv_column_list: str, flags: int, *args, **kwargs) -> int:
        """TODO: document"""

    @abstractmethod
    def export_json_entity_report(self, flags: int, *args, **kwargs) -> int:
        """TODO: document"""

    @abstractmethod
    def fetch_next(self, response_handle: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_interesting_entities_by_entity_id(self, entity_id: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_interesting_entities_by_record_id(self, data_source_code: str, record_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_network_by_entity_id_v2(self, entity_list: str, max_degree: int, build_out_degree: int, max_entities: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_network_by_entity_id(self, entity_list: str, max_degree: int, build_out_degree: int, max_entities: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_network_by_record_id_v2(self, record_list: str, max_degree: int, build_out_degree: int, max_entities: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_network_by_record_id(self, record_list: str, max_degree: int, build_out_degree: int, max_entities: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_by_entity_id_v2(self, entity_id_1: int, entity_id_2: int, max_degree: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_by_entity_id(self, entity_id_1: int, entity_id_2: int, max_degree: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_by_record_id_v2(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, max_degree: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_by_record_id(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, max_degree: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_excluding_by_entity_id_v2(self, entity_id_1: int, entity_id_2: int, max_degree: int, excluded_entities: str, flags: str, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_excluding_by_entity_id(self, entity_id_1: int, entity_id_2: int, max_degree: int, excluded_entities: str, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_excluding_by_record_id_v2(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, max_degree: int, excluded_records: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_excluding_by_record_id(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, max_degree: int, excluded_records: str, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_including_source_by_entity_id_v2(self, entity_id_1: int, entity_id_2: int, max_degree: int, excluded_entities: str, required_dsrcs: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_including_source_by_entity_id(self, entity_id_1: int, entity_id_2: int, max_degree: int, excluded_entities: str, required_dsrcs: str, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_including_source_by_record_id_v2(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, max_degree: int, excluded_records: str, required_dsrcs: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_including_source_by_record_id(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, max_degree: int, excluded_records: str, required_dsrcs: str, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def get_active_config_id(self, *args, **kwargs) -> int:
        """TODO: document"""

    @abstractmethod
    def get_entity_by_entity_id_v2(self, entity_id: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def get_entity_by_entity_id(self, entity_id: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def get_entity_by_record_id_v2(self, data_source_code: str, record_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def get_entity_by_record_id(self, data_source_code: str, record_id: str, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def get_record_v2(self, data_source_code: str, record_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def get_record(self, data_source_code: str, record_id: str, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def get_redo_record(self, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def get_repository_last_modified_time(self, *args, **kwargs) -> int:
        """TODO: document"""

    @abstractmethod
    def get_virtual_entity_by_record_id_v2(self, record_list: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def get_virtual_entity_by_record_id(self, record_list: str, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def how_entity_by_entity_id_v2(self, entity_id: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def how_entity_by_entity_id(self, entity_id: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def init(self, module_name: str, ini_params: str, verbose_logging: int, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def init_with_config_id(self, module_name: str, ini_params: str, init_config_id: int, verbose_logging: int, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def prime_engine(self, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def process(self, record: str, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def process_with_info(self, record: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def purge_repository(self, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def reevaluate_entity(self, entity_id: int, flags: int, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def reevaluate_entity_with_info(self, entity_id: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def reevaluate_record(self, data_source_code: str, record_id: str, flags: int, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def reevaluate_record_with_info(self, data_source_code: str, record_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def reinit(self, init_config_id: int, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def replace_record(self, data_source_code: str, record_id: str, json_data: str, load_id: str, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def replace_record_with_info(self, data_source_code: str, record_id: str, json_data: str, load_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def search_by_attributes_v2(self, json_data: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def search_by_attributes(self, json_data: str, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def stats(self, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def why_entities_v2(self, entity_id_1: int, entity_id_2: int, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def why_entities(self, entity_id_1: int, entity_id_2: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def why_entity_by_entity_id_v2(self, entity_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def why_entity_by_entity_id(self, entity_id: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def why_entity_by_record_id_v2(self, data_source_code: str, record_id: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def why_entity_by_record_id(self, data_source_code: str, record_id: str, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def why_records_v2(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, flags: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def why_records(self, data_source_code_1: str, record_id_1: str, data_source_code_2: str, record_id_2: str, *args, **kwargsr) -> str:
        """TODO: document"""

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------

    def get_record_as_dict(self, data_source_code: str, record_id: str, *args, **kwargs) -> dict:
        """TODO: document"""
        return json.loads(self.get_record(data_source_code, record_id, args, kwargs))
