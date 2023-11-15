#! /usr/bin/env python3

"""
TODO: g2engine_abstract.py
"""

# Import from standard library. https://docs.python.org/3/library/

import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple, cast

from .g2engineflags import G2EngineFlags

# Metadata

__all__ = ["G2EngineAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"


class G2EngineAbstract(ABC):
    """
    G2 diagnostic module access library
    """

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    # TODO: Change to f-strings
    # Change to be same as g2Product: G2Engine_<method_name()>
    PREFIX = "g2engine."
    """ :meta private: """

    ID_MESSAGES = {
        4001: PREFIX + "G2_addRecord({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4002: PREFIX
        + "G2_addRecordWithInfo({0}, {1}, {2}, {3}, {4}) failed. Return code: {5}",
        4003: PREFIX
        + "G2_addRecordWithInfoWithReturnedRecordID({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4004: PREFIX
        + "G2_addRecordWithReturnedRecordID({0}, {1}, {2}) failed. Return code: {3}",
        4005: PREFIX + "G2_checkRecord({0}, {1}) failed. Return code: {2}",
        4006: PREFIX + "G2_closeExport({0}) failed. Return code: {1}",
        4007: PREFIX + "G2_deleteRecord({0}, {1}, {2}) failed. Return code: {3}",
        4008: PREFIX
        + "G2_deleteRecordWithInfo({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4009: PREFIX + "G2_destroy() failed. Return code: {0}",
        4010: PREFIX + "G2_exportConfigAndConfigID() failed. Return code: {0}",
        4011: PREFIX + "G2_exportConfig() failed. Return code: {0}",
        4012: PREFIX + "G2_exportCSVEntityReport({0}, {1}) failed. Return code: {2}",
        4013: PREFIX + "G2_exportJSONEntityReport({0}) failed. Return code: {1}",
        4014: PREFIX + "G2_fetchNext({0}) failed. Return code: {1}",
        4015: PREFIX
        + "G2_findInterestingEntitiesByEntityID({0}, {1}) failed. Return code: {2}",
        4016: PREFIX
        + "G2_findInterestingEntitiesByRecordID({0}, {1}, {2}) failed. Return code: {3}",
        4017: PREFIX
        + "G2_findNetworkByEntityID({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4018: PREFIX
        + "G2_findNetworkByEntityID_V2({0}, {1}, {2}, {3}, {4}) failed. Return code: {5}",
        4019: PREFIX
        + "G2_findNetworkByRecordID({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4020: PREFIX
        + "G2_findNetworkByRecordID_V2({0}, {1}, {2}, {3}, {4}) failed. Return code: {5}",
        4021: PREFIX + "G2_findPathByEntityID({0}, {1}, {2}) failed. Return code: {3}",
        4022: PREFIX
        + "G2_findPathByEntityID_V2({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4023: PREFIX
        + "G2_findPathByRecordID({0}, {1}, {2}, {3}, {4}) failed. Return code: {5}",
        4024: PREFIX
        + "G2_findPathByRecordID_V2({0}, {1}, {2}, {3}, {4}, {5}) failed. Return code: {0}",
        4025: PREFIX
        + "G2_findPathExcludingByEntityID({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4026: PREFIX
        + "G2_findPathExcludingByEntityID_V2({0}, {1}, {2}, {3}, {4}) failed. Return code: {5}",
        4027: PREFIX
        + "G2_findPathExcludingByRecordID({0}, {1}, {2}, {3} {4}, {5}) failed. Return code: {6}",
        4028: PREFIX
        + "G2_findPathExcludingByRecordID_V2({0}, {1}, {2}, {3} {4}, {5}, {6}) failed. Return code: {7}",
        4029: PREFIX
        + "G2_findPathIncludingSourceByEntityID({0}, {1}, {2}, {3}, {4}) failed. Return code: {5}",
        4030: PREFIX
        + "G2_findPathIncludingSourceByEntityID_V2({0}, {1}, {2}, {3}, {4}, {5}) failed. Return code: {6}",
        4031: PREFIX
        + "G2_findPathIncludingSourceByRecordID({0}, {1}, {2}, {3} {4}, {5}, {6}) failed. Return code: {7}",
        4032: PREFIX
        + "G2_findPathIncludingSourceByRecordID_V2({0}, {1}, {2}, {3} {4}, {5}, {6}, {7}) failed. Return code: {8}",
        4033: PREFIX + "G2_getActiveConfigID() failed. Return code: {0}",
        # TODO Modified to reflect V4
        # 4034: PREFIX + "G2_getEntityByEntityID({0}) failed. Return code: {1}",
        4034: PREFIX + "G2_getEntityByEntityID({0}, {1}) failed. Return code: {2}",
        4035: PREFIX + "G2_getEntityByEntityID_V2({0}, {1}) failed. Return code: {2}",
        4036: PREFIX + "G2_getEntityByRecordID({0}, {1}) failed. Return code: {2}",
        4037: PREFIX
        + "G2_getEntityByRecordID_V2({0}, {1}, {2}) failed. Return code: {3}",
        4038: PREFIX + "G2_getLastException() failed. Return code: {0}",
        4039: PREFIX + "G2_getRecord({0}, {1}) failed. Return code: {2}",
        4040: PREFIX + "G2_getRecord_V2({0}, {1}, {2}) failed. Return code: {3}",
        4041: PREFIX + "G2_getRedoRecord() failed. Return code: {0}",
        4042: PREFIX + "G2_getRepositoryLastModifiedTime() failed. Return code: {0}",
        4043: PREFIX + "G2_getVirtualEntityByRecordID({0}) failed. Return code: {1}",
        4044: PREFIX
        + "G2_getVirtualEntityByRecordID_V2({0}, {1}) failed. Return code: {2}",
        4045: PREFIX + "G2_howEntityByEntityID({0}) failed. Return code: {1}",
        4046: PREFIX + "G2_howEntityByEntityID_V2({0}, {1}) failed. Return code: {2}",
        4047: PREFIX + "G2_init({0}, {1}, {2}) failed. Return code: {3}",
        4048: PREFIX
        + "G2_initWithConfigID({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4049: PREFIX + "G2_primeEngine() failed. Return code: {0}",
        4050: PREFIX + "G2_process({0}) failed. Return code: {1}",
        4051: PREFIX + "G2_processRedoRecord() failed. Return code: {0}",
        4052: PREFIX + "G2_processRedoRecordWithInfo({0}) failed. Return code: {0}",
        4053: PREFIX + "G2_processWithInfo({0}, {1}) failed. Return code: {2}",
        4054: PREFIX + "G2_processWithResponse({0}) failed. Return code: {1}",
        4055: PREFIX + "G2_processWithResponseResize({0}) failed. Return code: {1}",
        4056: PREFIX + "G2_purgeRepository() failed. Return code: {0}",
        4057: PREFIX + "G2_reevaluateEntity({0}, {1}) failed. Return code: {2}",
        4058: PREFIX + "G2_reevaluateEntityWithInfo({0}, {1}) failed. Return code: {2}",
        4059: PREFIX + "G2_reevaluateRecord({0}, {1}, {2}) failed. Return code: {3}",
        4060: PREFIX
        + "G2_reevaluateRecordWithInfo({0}, {1}, {2}) failed. Return code: {3}",
        4061: PREFIX + "G2_reinit({0}) failed. Return code: {1}",
        4062: PREFIX + "G2_replaceRecord({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4063: PREFIX
        + "G2_replaceRecordWithInfo({0}, {1}, {2}, {3}, {4}) failed. Return code: {5}",
        4064: PREFIX + "G2_searchByAttributes({0}) failed. Return code: {5}",
        4065: PREFIX + "G2_searchByAttributes_V2({0}, {1}) failed. Return code: {2}",
        4066: PREFIX + "G2_stats() failed. Return code: {0}",
        4067: PREFIX + "G2_whyEntities({0}, {1}) failed. Return code: {2}",
        4068: PREFIX + "G2_whyEntities_V2({0}, {1}, {2}) failed. Return code: {3}",
        4069: PREFIX + "G2_whyEntityByEntityID({0}) failed. Return code: {1}",
        4070: PREFIX + "G2_whyEntityByEntityID_V2({0}, {1}) failed. Return code: {2}",
        4071: PREFIX + "G2_whyEntityByRecordID({0}, {1}) failed. Return code: {2}",
        4072: PREFIX
        + "G2_whyEntityByRecordID_V2({0}, {1}, {2}) failed. Return code: {3}",
        4073: PREFIX + "G2_whyRecords({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4074: PREFIX
        + "G2_whyRecords_V2({0}, {1}, {2}, {3}, {4}) failed. Return code: {5}",
        4075: PREFIX
        + "G2Engine{0}, {1}) failed. module_name and ini_params must both be set or both be empty",
    }
    """ :meta private: """

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def add_record(
        self,
        data_source_code: str,
        record_id: str,
        json_data: str,
        # TODO: load_id is no longer used, being removed from V4 C api?
        load_id: str = "",
        **kwargs: Any,
    ) -> None:
        """
        The `add_record` method adds a record into the Senzing repository.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            json_data (str): A JSON document containing the record to be added to the Senzing repository.
            load_id (str, optional): A JSON document containing the record to be added to the Senzing repository. Defaults to "".

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2engine/add_record.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def add_record_with_info(
        self,
        data_source_code: str,
        record_id: str,
        json_data: str,
        # TODO: load_id is no longer used, being removed from V4 C api?
        load_id: str = "",
        flags: int = 0,
        **kwargs: Any,
    ) -> str:
        """
        The `add_record_with_info` method adds a record into the Senzing repository and returns information on the affected entities.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            json_data (str): A JSON document containing the record to be added to the Senzing repository.
            load_id (str, optional): A JSON document containing the record to be added to the Senzing repository. Defaults to "".
            flags (int, optional): Flags used to control information returned. Defaults to 0.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2engine/add_record_with_info.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2engine/add_record_with_info.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def close_export(self, response_handle: int, **kwargs: Any) -> None:
        """
        The `close_export` method closes the exported document created by `export_json_entity_report`.
        It is part of the `export_json_entity_report`, `fetch_next`, `close_export`
        lifecycle of a list of sized entities.

        Args:
            response_handle (int): A handle created by `export_json_entity_report` or `export_csv_entity_report`.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2engine/export_fetch_close.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2engine/export_fetch_close.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def count_redo_records(self, **kwargs: Any) -> int:
        """
        The `count_redo_records` method returns the number of records in need of redo-ing.

        Returns:
            int: The number of redo records in Senzing's redo queue.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2engine/count_redo_records.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def delete_record(
        self,
        data_source_code: str,
        record_id: str,
        # TODO: load_id is no longer used, being removed from V4 C api?
        load_id: str = "",
        **kwargs: Any,
    ) -> None:
        """
        The `delete_record` method deletes a record from the Senzing repository.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            load_id (str, optional): An identifier used to distinguish different load batches/sessions. An empty string is acceptable. Defaults to "".

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2engine/delete_record.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def delete_record_with_info(
        self,
        data_source_code: str,
        record_id: str,
        # TODO: load_id is no longer used, being removed from V4 C api?
        load_id: str = "",
        flags: int = 0,
        **kwargs: Any,
    ) -> str:
        """
        The `delete_record_with_info` method deletes a record from the Senzing repository and returns information on the affected entities.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            load_id (str, optional): An identifier used to distinguish different load batches/sessions. An empty string is acceptable. Defaults to "".
            flags (int, optional): Flags used to control information returned.. Defaults to 0.

        Returns:
            str: Flags used to control information returned.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2engine/delete_record_with_info.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2engine/delete_record_with_info.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def destroy(self, **kwargs: Any) -> None:
        """
        The `destroy` method will destroy and perform cleanup for the Senzing G2Engine object.
        It should be called after all other calls are complete.

        **Note:** If the `G2Engine` constructor was called with parameters,
        the destructor will automatically call the destroy() method.
        In this case, a separate call to `destroy()` is not needed.

        Example:

        .. code-block:: python

            g2_engine = g2engine.G2Engine(module_name, ini_params)

        Raises:
            g2exception.G2Exception:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2engine/g2engine_init_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def export_config(self, **kwargs: Any) -> str:
        """
        The `export_config` method returns the Senzing engine configuration.

        Returns:
            str: A JSON document containing the current Senzing Engine configuration.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2engine/export_config.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2engine/export_config.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def export_config_and_config_id(self, **kwargs: Any) -> Tuple[str, int]:
        """
        Similar to `export_config`, the `export_config_and_config_id` method returns the Senzing engine configuration and it's identifier.

        Returns:
            Tuple[str, int]: [A JSON document containing the current Senzing Engine configuration, The unique identifier of the Senzing Engine configuration]

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2engine/export_config_and_config_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2engine/export_config_and_config_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def export_csv_entity_report(
        self,
        csv_column_list: str,
        flags: int = G2EngineFlags.G2_EXPORT_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> int:
        """TODO: document"""

    @abstractmethod
    def export_json_entity_report(
        self, flags: int = G2EngineFlags.G2_EXPORT_DEFAULT_FLAGS, **kwargs: Any
    ) -> int:
        """TODO: document"""

    @abstractmethod
    def fetch_next(self, response_handle: int, **kwargs: Any) -> str:
        """TODO: document"""

    @abstractmethod
    def find_interesting_entities_by_entity_id(
        self, entity_id: int, flags: int = 0, **kwargs: Any
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def find_interesting_entities_by_record_id(
        self, data_source_code: str, record_id: str, flags: int = 0, **kwargs: Any
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def find_network_by_entity_id_v2(
        self,
        entity_list: str,
        max_degree: int,
        build_out_degree: int,
        max_entities: int,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def find_network_by_entity_id(
        self,
        entity_list: str,
        max_degree: int,
        build_out_degree: int,
        max_entities: int,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def find_network_by_record_id_v2(
        self,
        record_list: str,
        max_degree: int,
        build_out_degree: int,
        max_entities: int,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def find_network_by_record_id(
        self,
        record_list: str,
        max_degree: int,
        build_out_degree: int,
        max_entities: int,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def find_path_by_entity_id_v2(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_by_entity_id(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def find_path_by_record_id_v2(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_by_record_id(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def find_path_excluding_by_entity_id_v2(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        excluded_entities: str,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_excluding_by_entity_id(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        excluded_entities: str,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def find_path_excluding_by_record_id_v2(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        excluded_records: str,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_excluding_by_record_id(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        excluded_records: str,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def find_path_including_source_by_entity_id_v2(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        excluded_entities: str,
        required_dsrcs: str,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_including_source_by_entity_id(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        excluded_entities: str,
        required_dsrcs: str,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def find_path_including_source_by_record_id_v2(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        excluded_records: str,
        required_dsrcs: str,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def find_path_including_source_by_record_id(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        excluded_records: str,
        required_dsrcs: str,
        flags: int = G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def get_active_config_id(self, **kwargs: Any) -> int:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def get_entity_by_entity_id_v2(
        self,
        entity_id: int,
        flags: int = G2EngineFlags.G2_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def get_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = G2EngineFlags.G2_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def get_entity_by_record_id_v2(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = G2EngineFlags.G2_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def get_entity_by_record_id(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = G2EngineFlags.G2_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def get_record_v2(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = G2EngineFlags.G2_RECORD_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def get_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = G2EngineFlags.G2_RECORD_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def get_redo_record(self, **kwargs: Any) -> str:
        """TODO: document"""

    @abstractmethod
    def get_repository_last_modified_time(self, **kwargs: Any) -> int:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def get_virtual_entity_by_record_id_v2(
        self,
        record_list: str,
        flags: int = G2EngineFlags.G2_HOW_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def get_virtual_entity_by_record_id(
        self,
        record_list: str,
        flags: int = G2EngineFlags.G2_HOW_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def how_entity_by_entity_id_v2(
        self,
        entity_id: int,
        flags: int = G2EngineFlags.G2_HOW_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def how_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = G2EngineFlags.G2_HOW_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def init(
        self, module_name: str, ini_params: str, verbose_logging: int = 0, **kwargs: Any
    ) -> None:
        """TODO: document"""

    @abstractmethod
    def init_with_config_id(
        self,
        module_name: str,
        ini_params: str,
        init_config_id: int,
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        """TODO: document"""

    @abstractmethod
    def prime_engine(self, **kwargs: Any) -> None:
        """TODO: document"""

    @abstractmethod
    def process(self, record: str, **kwargs: Any) -> None:
        """TODO: document"""

    @abstractmethod
    def process_with_info(self, record: str, flags: int, **kwargs: Any) -> str:
        """TODO: document"""

    @abstractmethod
    def purge_repository(self, **kwargs: Any) -> None:
        """TODO: document"""

    @abstractmethod
    def reevaluate_entity(self, entity_id: int, flags: int = 0, **kwargs: Any) -> None:
        """TODO: document"""

    @abstractmethod
    def reevaluate_entity_with_info(
        self, entity_id: int, flags: int = 0, **kwargs: Any
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def reevaluate_record(
        self, data_source_code: str, record_id: str, flags: int = 0, **kwargs: Any
    ) -> None:
        """TODO: document"""

    @abstractmethod
    def reevaluate_record_with_info(
        self, data_source_code: str, record_id: str, flags: int = 0, **kwargs: Any
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def reinit(self, init_config_id: int, **kwargs: Any) -> None:
        """TODO: document"""

    @abstractmethod
    def replace_record(
        self,
        data_source_code: str,
        record_id: str,
        json_data: str,
        # TODO: load_id is no longer used, being removed from V4 C api?
        load_id: None = None,
        **kwargs: Any,
    ) -> None:
        """TODO: document"""

    @abstractmethod
    def replace_record_with_info(
        self,
        data_source_code: str,
        record_id: str,
        json_data: str,
        # TODO: load_id is no longer used, being removed from V4 C api?
        load_id: None = None,
        flags: int = 0,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def search_by_attributes_v2(
        self,
        json_data: str,
        flags: int = G2EngineFlags.G2_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def search_by_attributes_v3(
        self,
        json_data: str,
        search_profile: str,
        flags: int = G2EngineFlags.G2_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def search_by_attributes(
        self,
        json_data: str,
        flags: int = G2EngineFlags.G2_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def stats(self, **kwargs: Any) -> str:
        """TODO: document"""

    @abstractmethod
    def why_entities_v2(
        self,
        entity_id_1: int,
        entity_id_2: int,
        flags: int = G2EngineFlags.G2_WHY_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def why_entities(
        self,
        entity_id_1: int,
        entity_id_2: int,
        flags: int = G2EngineFlags.G2_WHY_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def why_entity_by_entity_id_v2(
        self,
        entity_id: str,
        flags: int = G2EngineFlags.G2_WHY_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def why_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = G2EngineFlags.G2_WHY_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def why_entity_by_record_id_v2(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = G2EngineFlags.G2_WHY_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def why_entity_by_record_id(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = G2EngineFlags.G2_WHY_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: This should be going away in V4?
    @abstractmethod
    def why_records_v2(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        flags: int = G2EngineFlags.G2_WHY_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def why_records(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        flags: int = G2EngineFlags.G2_WHY_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """TODO: document"""

    # TODO: Is why_record_in_entity missing?

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------

    def get_record_as_dict(
        # self, data_source_code: str, record_id: str, **kwargs: Any
        self,
        data_source_code: str,
        record_id: str,
        flags: int = G2EngineFlags.G2_RECORD_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: document"""
        return cast(
            Dict[str, Any],
            json.loads(self.get_record(data_source_code, record_id, flags, **kwargs)),
        )
