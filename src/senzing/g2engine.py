#! /usr/bin/env python3

"""
TODO: g2engine.py
"""

import ctypes
import os
from typing import Any, Tuple

from .g2engine_abstract import G2EngineAbstract
from .g2exception import G2Exception, new_g2exception
from .g2helpers import find_file_in_path

# Metadata

__all__ = ["G2Engine"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

SENZING_PRODUCT_ID = "5043"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md
CALLER_SKIP = 6

# -----------------------------------------------------------------------------
# Classes that are result structures from calls to Senzing
# -----------------------------------------------------------------------------

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

    def __init__(
        self,
        module_name: str,
        ini_params: str,
        verbose_logging: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """

        self.ini_params = ini_params
        self.module_name = module_name
        self.noop = ""
        self.verbose_logging = verbose_logging

        try:
            if os.name == "nt":
                self.library_handle = ctypes.cdll.LoadLibrary(
                    find_file_in_path("G2.dll")
                )
            else:
                self.library_handle = ctypes.cdll.LoadLibrary("libG2.so")
        except OSError as err:
            raise G2Exception("Failed to load the G2 library") from err

        # Initialize C function input parameters and results.
        # Must be synchronized with g2/sdk/c/libg2engine.h

        self.library_handle.G2Engine_clearLastException.argtypes = []
        self.library_handle.G2Engine_clearLastException.restype = None
        self.library_handle.G2Engine_getLastException.argtypes = [
            ctypes.POINTER(ctypes.c_char),
            ctypes.c_size_t,
        ]
        self.library_handle.G2Engine_getLastException.restype = ctypes.c_longlong
        self.library_handle.G2GoHelper_free.argtypes = [ctypes.c_char_p]

        # Initialize Senzing engine.

        self.init(self.module_name, self.ini_params, self.verbose_logging)

    def __del__(self) -> None:
        """Destructor"""
        self.destroy()

    # -------------------------------------------------------------------------
    # Development methods - to be removed after initial development
    # -------------------------------------------------------------------------

    def fake_g2engine(self, *args: Any, **kwargs: Any) -> None:
        """
        TODO: Remove once SDK methods have been implemented.

        :meta private:
        """
        if len(args) + len(kwargs) > 2000:
            print(self.noop)

    # -------------------------------------------------------------------------
    # Exception helpers
    # -------------------------------------------------------------------------

    def new_exception(self, error_id: int, *args: Any) -> Exception:
        """
        Generate a new exception based on the error_id.

        :meta private:
        """
        return new_g2exception(
            self.library_handle.G2Engine_getLastException,
            self.library_handle.G2Engine_clearLastException,
            SENZING_PRODUCT_ID,
            error_id,
            self.ID_MESSAGES,
            CALLER_SKIP,
            *args,
        )

    # -------------------------------------------------------------------------
    # G2Engine methods
    # -------------------------------------------------------------------------

    def add_record(
        self,
        data_source_code: str,
        record_id: str,
        json_data: str,
        load_id: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.fake_g2engine(data_source_code, record_id, json_data, load_id)

    def add_record_with_info(
        self,
        data_source_code: str,
        record_id: str,
        json_data: str,
        load_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, json_data, load_id, flags)
        return "string"

    def close_export(self, response_handle: int, *args: Any, **kwargs: Any) -> None:
        self.fake_g2engine(response_handle)

    def count_redo_records(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2engine()
        return 0

    def delete_record(
        self,
        data_source_code: str,
        record_id: str,
        load_id: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.fake_g2engine(data_source_code, record_id, load_id)

    def delete_record_with_info(
        self,
        data_source_code: str,
        record_id: str,
        load_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, load_id, flags)
        return "string"

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        self.fake_g2engine()

    def export_config(self, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine()
        return "string"

    def export_config_and_config_id(self, *args: Any, **kwargs: Any) -> Tuple[str, int]:
        self.fake_g2engine()
        return "string", 0

    def export_csv_entity_report(
        self, csv_column_list: str, flags: int, *args: Any, **kwargs: Any
    ) -> int:
        self.fake_g2engine(csv_column_list, flags)
        return 0

    def export_json_entity_report(self, flags: int, *args: Any, **kwargs: Any) -> int:
        self.fake_g2engine(flags)
        return 0

    def fetch_next(self, response_handle: int, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine(response_handle)
        return "string"

    def find_interesting_entities_by_entity_id(
        self, entity_id: int, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(entity_id, flags)
        return "string"

    def find_interesting_entities_by_record_id(
        self,
        data_source_code: str,
        record_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def find_network_by_entity_id_v2(
        self,
        entity_list: str,
        max_degree: int,
        build_out_degree: int,
        max_entities: int,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            entity_list, max_degree, build_out_degree, max_entities, flags
        )
        return "string"

    def find_network_by_entity_id(
        self,
        entity_list: str,
        max_degree: int,
        build_out_degree: int,
        max_entities: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(entity_list, max_degree, build_out_degree, max_entities)
        return "string"

    def find_network_by_record_id_v2(
        self,
        record_list: str,
        max_degree: int,
        build_out_degree: int,
        max_entities: int,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            record_list, max_degree, build_out_degree, max_entities, flags
        )
        return "string"

    def find_network_by_record_id(
        self,
        record_list: str,
        max_degree: int,
        build_out_degree: int,
        max_entities: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(record_list, max_degree, build_out_degree, max_entities)
        return "string"

    def find_path_by_entity_id_v2(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(entity_id_1, entity_id_2, max_degree, flags)
        return "string"

    def find_path_by_entity_id(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(entity_id_1, entity_id_2, max_degree)
        return "string"

    def find_path_by_record_id_v2(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1,
            record_id_1,
            data_source_code_2,
            record_id_2,
            max_degree,
            flags,
        )
        return "string"

    def find_path_by_record_id(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1, record_id_1, data_source_code_2, record_id_2, max_degree
        )
        return "string"

    def find_path_excluding_by_entity_id_v2(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        excluded_entities: str,
        flags: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            entity_id_1, entity_id_2, max_degree, excluded_entities, flags
        )
        return "string"

    def find_path_excluding_by_entity_id(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        excluded_entities: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(entity_id_1, entity_id_2, max_degree, excluded_entities)
        return "string"

    def find_path_excluding_by_record_id_v2(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        excluded_records: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1,
            record_id_1,
            data_source_code_2,
            record_id_2,
            max_degree,
            excluded_records,
            flags,
        )
        return "string"

    def find_path_excluding_by_record_id(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        excluded_records: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1,
            record_id_1,
            data_source_code_2,
            record_id_2,
            max_degree,
            excluded_records,
        )
        return "string"

    def find_path_including_source_by_entity_id_v2(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        excluded_entities: str,
        required_dsrcs: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            entity_id_1,
            entity_id_2,
            max_degree,
            excluded_entities,
            required_dsrcs,
            flags,
        )
        return "string"

    def find_path_including_source_by_entity_id(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        excluded_entities: str,
        required_dsrcs: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            entity_id_1, entity_id_2, max_degree, excluded_entities, required_dsrcs
        )
        return "string"

    def find_path_including_source_by_record_id_v2(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        excluded_records: str,
        required_dsrcs: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1,
            record_id_1,
            data_source_code_2,
            record_id_2,
            max_degree,
            excluded_records,
            required_dsrcs,
            flags,
        )
        return "string"

    def find_path_including_source_by_record_id(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        excluded_records: str,
        required_dsrcs: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1,
            record_id_1,
            data_source_code_2,
            record_id_2,
            max_degree,
            excluded_records,
            required_dsrcs,
        )
        return "string"

    def get_active_config_id(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2engine()
        return 0

    def get_entity_by_entity_id_v2(
        self, entity_id: int, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(entity_id, flags)
        return "string"

    def get_entity_by_entity_id(self, entity_id: int, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine(entity_id)
        return "string"

    def get_entity_by_record_id_v2(
        self,
        data_source_code: str,
        record_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def get_entity_by_record_id(
        self, data_source_code: str, record_id: str, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(data_source_code, record_id)
        return "string"

    def get_record_v2(
        self,
        data_source_code: str,
        record_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def get_record(
        self, data_source_code: str, record_id: str, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(data_source_code, record_id)
        return "string"

    def get_redo_record(self, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine()
        return "string"

    def get_repository_last_modified_time(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2engine()
        return 0

    def get_virtual_entity_by_record_id_v2(
        self, record_list: str, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(record_list, flags)
        return "string"

    def get_virtual_entity_by_record_id(
        self, record_list: str, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(record_list)
        return "string"

    def how_entity_by_entity_id_v2(
        self, entity_id: int, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(entity_id, flags)
        return "string"

    def how_entity_by_entity_id(self, entity_id: int, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine(entity_id)
        return "string"

    def init(
        self,
        module_name: str,
        ini_params: str,
        verbose_logging: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.fake_g2engine(module_name, ini_params, verbose_logging)

    def init_with_config_id(
        self,
        module_name: str,
        ini_params: str,
        init_config_id: int,
        verbose_logging: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.fake_g2engine(module_name, ini_params, init_config_id, verbose_logging)

    def prime_engine(self, *args: Any, **kwargs: Any) -> None:
        self.fake_g2engine()

    def process(self, record: str, *args: Any, **kwargs: Any) -> None:
        self.fake_g2engine(record)

    def process_with_info(
        self, record: str, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(record, flags)
        return "string"

    def purge_repository(self, *args: Any, **kwargs: Any) -> None:
        self.fake_g2engine()

    def reevaluate_entity(
        self, entity_id: int, flags: int, *args: Any, **kwargs: Any
    ) -> None:
        self.fake_g2engine(entity_id, flags)

    def reevaluate_entity_with_info(
        self, entity_id: int, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(entity_id, flags)
        return "string"

    def reevaluate_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.fake_g2engine(data_source_code, record_id, flags)

    def reevaluate_record_with_info(
        self,
        data_source_code: str,
        record_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def reinit(self, init_config_id: int, *args: Any, **kwargs: Any) -> None:
        self.fake_g2engine(init_config_id)

    def replace_record(
        self,
        data_source_code: str,
        record_id: str,
        json_data: str,
        load_id: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.fake_g2engine(data_source_code, record_id, json_data, load_id)

    def replace_record_with_info(
        self,
        data_source_code: str,
        record_id: str,
        json_data: str,
        load_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, json_data, load_id, flags)
        return "string"

    def search_by_attributes_v2(
        self, json_data: str, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(json_data, flags)
        return "string"

    def search_by_attributes(self, json_data: str, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine(json_data)
        return "string"

    def stats(self, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine()
        return "string"

    def why_entities_v2(
        self, entity_id_1: int, entity_id_2: int, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(entity_id_1, entity_id_2, flags)
        return "string"

    def why_entities(
        self, entity_id_1: int, entity_id_2: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(entity_id_1, entity_id_2)
        return "string"

    def why_entity_by_entity_id_v2(
        self, entity_id: str, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(entity_id, flags)
        return "string"

    def why_entity_by_entity_id(self, entity_id: int, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine(entity_id)
        return "string"

    def why_entity_by_record_id_v2(
        self,
        data_source_code: str,
        record_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def why_entity_by_record_id(
        self, data_source_code: str, record_id: str, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(data_source_code, record_id)
        return "string"

    def why_records_v2(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1, record_id_1, data_source_code_2, record_id_2, flags
        )
        return "string"

    def why_records(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1, record_id_1, data_source_code_2, record_id_2
        )
        return "string"
