"""
TODO: Create documentation
"""

# NOTE Used for ctypes type hinting - https://stackoverflow.com/questions/77619149/python-ctypes-pointer-type-hinting
from __future__ import annotations

import json
from types import TracebackType
from typing import Any, Callable, Dict, Optional, Type, Union

from senzing_abstract import SzEngineAbstract

from senzing import SzEngineFlags
from senzing._helpers import as_str

# Metadata

__all__ = ["SzEngine"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2024-05-03"
__updated__ = "2024-05-03"


def default_dict_function(input_string: str) -> Dict[str, Any]:
    """TODO: Create documentation"""
    result: Dict[str, Any] = json.loads(input_string)
    return result


# -----------------------------------------------------------------------------
# SzEngine class
# -----------------------------------------------------------------------------


class SzEngine:
    """
    TODO: Create documentation
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        sz_engine: SzEngineAbstract,
        dict_function: Callable[[str], Dict[str, Any]] = default_dict_function,
        **kwargs: Any,
    ) -> None:
        """TODO: Create documentation"""

        self.sz_engine = sz_engine
        self.dict_function = dict_function
        _ = kwargs

    def __enter__(
        self,
    ) -> (
        Any
    ):  # TODO: Replace "Any" with "Self" once python 3.11 is lowest supported python version.
        """Context Manager method."""
        return self

    def __exit__(
        self,
        exc_type: Union[Type[BaseException], None],
        exc_val: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ) -> None:
        """Context Manager method."""

    # -------------------------------------------------------------------------
    # SzEngine methods
    # -------------------------------------------------------------------------

    def add_record(
        self,
        data_source_code: str,
        record_id: str,
        record_definition: Union[str, Dict[Any, Any]],
        flags: int = 0,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.add_record(
                data_source_code, record_id, as_str(record_definition), flags, **kwargs
            )
        )

    def close_export(self, export_handle: int, **kwargs: Any) -> None:
        """TODO: Create documentation"""
        return self.sz_engine.close_export(export_handle, **kwargs)

    def count_redo_records(self, **kwargs: Any) -> int:
        """TODO: Create documentation"""
        return self.sz_engine.count_redo_records(**kwargs)

    def delete_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = 0,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.delete_record(data_source_code, record_id, flags, **kwargs)
        )

    # TODO
    # def destroy(self, **kwargs: Any) -> None:
    #     """TODO: Create documentation"""
    #     return self.sz_engine.destroy(**kwargs)

    def export_csv_entity_report(
        self,
        csv_column_list: str,
        flags: int = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> int:
        """TODO: Create documentation"""
        return self.sz_engine.export_csv_entity_report(csv_column_list, flags, **kwargs)

    def export_json_entity_report(
        self,
        flags: int = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> int:
        """TODO: Create documentation"""
        return self.sz_engine.export_json_entity_report(flags, **kwargs)

    def fetch_next(self, export_handle: int, **kwargs: Any) -> str:
        """TODO: Create documentation"""
        return self.sz_engine.fetch_next(export_handle, **kwargs)

    def fetch_next_return_dict(
        self, export_handle: int, **kwargs: Any
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(self.sz_engine.fetch_next(export_handle, **kwargs))

    def find_interesting_entities_by_entity_id(
        self, entity_id: int, flags: int = 0, **kwargs: Any
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.find_interesting_entities_by_entity_id(
                entity_id, flags, **kwargs
            )
        )

    def find_interesting_entities_by_record_id(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = 0,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.find_interesting_entities_by_record_id(
                data_source_code, record_id, flags, **kwargs
            )
        )

    def find_network_by_entity_id(
        self,
        # TODO
        # entity_ids: Union[str, Dict[Any, Any]],
        entity_ids: list[int],
        max_degrees: int,
        build_out_degree: int,
        build_out_max_entities: int,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.find_network_by_entity_id(
                entity_ids,
                max_degrees,
                build_out_degree,
                build_out_max_entities,
                flags,
                **kwargs,
            )
        )

    def find_network_by_record_id(
        self,
        # record_keys: Union[str, Dict[str, List[Dict[str, str]]]],
        record_keys: list[tuple[str, str]],
        max_degrees: int,
        build_out_degree: int,
        build_out_max_entities: int,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.find_network_by_record_id(
                record_keys,
                max_degrees,
                build_out_degree,
                build_out_max_entities,
                flags,
                **kwargs,
            )
        )

    def find_path_by_entity_id(
        self,
        start_entity_id: int,
        end_entity_id: int,
        max_degrees: int,
        # exclusions: Union[str, Dict[Any, Any]] = "",
        # required_data_sources: Union[str, Dict[Any, Any]] = "",
        # TODO avoid_entity_ids, change by record too
        exclusions: Optional[list[int]] = None,
        required_data_sources: Optional[list[str]] = None,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.find_path_by_entity_id(
                start_entity_id,
                end_entity_id,
                max_degrees,
                exclusions,
                required_data_sources,
                flags,
                **kwargs,
            )
        )

    def find_path_by_record_id(
        self,
        start_data_source_code: str,
        start_record_id: str,
        end_data_source_code: str,
        end_record_id: str,
        max_degrees: int,
        # exclusions: Union[str, Dict[Any, Any]] = "",
        # required_data_sources: Union[str, Dict[Any, Any]] = "",
        exclusions: Optional[list[tuple[str, str]]] = None,
        required_data_sources: Optional[list[str]] = None,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.find_path_by_record_id(
                start_data_source_code,
                start_record_id,
                end_data_source_code,
                end_record_id,
                max_degrees,
                exclusions,
                required_data_sources,
                flags,
                **kwargs,
            )
        )

    def get_active_config_id(self, **kwargs: Any) -> int:
        """TODO: Create documentation"""
        return self.sz_engine.get_active_config_id(**kwargs)

    def get_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.get_entity_by_entity_id(
                entity_id,
                flags,
                **kwargs,
            )
        )

    def get_entity_by_record_id(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.get_entity_by_record_id(
                data_source_code,
                record_id,
                flags,
                **kwargs,
            )
        )

    def get_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.get_record(
                data_source_code,
                record_id,
                flags,
                **kwargs,
            )
        )

    def get_redo_record(self, **kwargs: Any) -> str:
        """TODO: Create documentation"""
        return self.sz_engine.get_redo_record(
            **kwargs,
        )

    def get_stats(self, **kwargs: Any) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.get_stats(
                **kwargs,
            )
        )

    def get_virtual_entity_by_record_id(
        self,
        # record_list: Union[str, Dict[Any, Any]],
        record_keys: list[tuple[str, str]],
        flags: int = SzEngineFlags.SZ_VIRTUAL_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.get_virtual_entity_by_record_id(
                record_keys,
                flags,
                **kwargs,
            )
        )

    def how_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_HOW_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.how_entity_by_entity_id(
                entity_id,
                flags,
                **kwargs,
            )
        )

    # TODO
    # def initialize(
    #     self,
    #     instance_name: str,
    #     settings: Union[str, Dict[Any, Any]],
    #     config_id: int = 0,
    #     verbose_logging: int = 0,
    #     **kwargs: Any,
    # ) -> None:
    #     """TODO: Create documentation"""
    #     return self.sz_engine.initialize(
    #         instance_name, settings, config_id, verbose_logging, **kwargs
    #     )

    def prime_engine(self, **kwargs: Any) -> None:
        """TODO: Create documentation"""
        return self.sz_engine.prime_engine(**kwargs)

    def process_redo_record(
        self, redo_record: str, flags: int = 0, **kwargs: Any
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.process_redo_record(
                redo_record,
                flags,
                **kwargs,
            )
        )

    def reevaluate_entity(
        self, entity_id: int, flags: int = 0, **kwargs: Any
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.reevaluate_entity(
                entity_id,
                flags,
                **kwargs,
            )
        )

    def reevaluate_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = 0,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.reevaluate_record(
                data_source_code,
                record_id,
                flags,
                **kwargs,
            )
        )

    def reinitialize(self, config_id: int, **kwargs: Any) -> None:
        """TODO: Create documentation"""
        return self.sz_engine.reinitialize(config_id, **kwargs)

    def search_by_attributes(
        self,
        attributes: Union[str, Dict[Any, Any]],
        search_profile: str = "",
        flags: int = SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.search_by_attributes(
                as_str(attributes),
                flags,
                search_profile,
                **kwargs,
            )
        )

    def why_entities(
        self,
        entity_id_1: int,
        entity_id_2: int,
        flags: int = SzEngineFlags.SZ_WHY_ENTITIES_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.why_entities(
                entity_id_1,
                entity_id_2,
                flags,
                **kwargs,
            )
        )

    def why_records(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        flags: int = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.why_records(
                data_source_code_1,
                record_id_1,
                data_source_code_2,
                record_id_2,
                flags,
                **kwargs,
            )
        )

    def why_record_in_entity(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_engine.why_record_in_entity(
                data_source_code,
                record_id,
                flags,
                **kwargs,
            )
        )
