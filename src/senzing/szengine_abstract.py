#! /usr/bin/env python3

"""
TODO: szengine_abstract.py
"""

# pylint: disable=C0302
# AC - Temp disables to get changes in for move to senzing garage
# pylint: disable=W0511,W1113


# Import from standard library. https://docs.python.org/3/library/

import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, cast

from .szengineflags import SzEngineFlags

# Metadata

# __all__ = ["G2EngineAbstract", "WithInfoResponsesAbstract"]
__all__ = ["SzEngineAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"


# -------------------------------------------------------------------------
# Classes
# -------------------------------------------------------------------------


class SzEngineAbstract(ABC):
    """
    Senzing engine module access library
    """

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    PREFIX = "szengine."
    """ :meta private: """

    ID_MESSAGES = {
        4001: PREFIX + "add_record({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4002: PREFIX + "close_export() failed. Return code: {0}",
        4003: PREFIX + "count_redo_records() failed. Return code: {0}",
        4004: PREFIX + "delete_record({0}, {1}, {2}) failed. Return code: {3}",
        4005: PREFIX + "destroy() failed. Return code: {0}",
        4006: PREFIX + "export_csv_entity_report({0}, {1}) failed. Return code: {2}",
        4007: PREFIX + "export_json_entity_report({0}) failed. Return code: {1}",
        4008: PREFIX + "fetch_next({0}) failed. Return code: {1}",
        # NOTE Included but not documented or examples, early adaptor feature, needs manual additions to config
        4009: PREFIX
        + "find_interesting_entities_by_entity_id({0}, {1}) failed. Return code: {2}",
        # NOTE Included but not documented or examples, early adaptor feature, needs manual additions to config
        4010: (
            PREFIX
            + "find_interesting_entities_by_record_id({0}, {1}, {2}) failed. Return"
            " code: {3}"
        ),
        4011: (
            PREFIX
            + "find_network_by_entity_id({0}, {1}, {2}, {3}, {4}) failed. Return code: {5}"
        ),
        4012: (
            PREFIX
            + "find_network_by_record_id({0}, {1}, {2}, {3}, {4}) failed. Return code: {5}"
        ),
        4013: PREFIX
        + "find_path_by_entity_id({0}, {1}, {2}, {3}, {4}, {5}) failed. Return code: {6}",
        4014: PREFIX
        + "find_path_by_record_id({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}) failed. Return code: {8}",
        4015: PREFIX + "get_active_config_id() failed. Return code: {0}",
        4016: PREFIX + "get_entity_by_entity_id({0}, {1}) failed. Return code: {2}",
        4017: PREFIX
        + "get_entity_by_record_id({0}, {1}, {3}) failed. Return code: {4}",
        4018: PREFIX + "get_record({0}, {1}, {2}) failed. Return code: {3}",
        4019: PREFIX + "get_redo_record() failed. Return code: {0}",
        4020: PREFIX + "get_repository_last_modified_time() failed. Return code: {0}",
        4021: PREFIX + "get_stats() failed. Return code: {0}",
        4022: PREFIX + "get_virtual_entity_by_record_id({0}) failed. Return code: {1}",
        4023: PREFIX + "how_entity_by_entity_id({0}) failed. Return code: {1}",
        4024: PREFIX + "initialize({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4025: PREFIX + "prime_engine() failed. Return code: {0}",
        4026: PREFIX + "process_redo_record({0}, {1}) failed. Return code: {2}",
        4027: PREFIX + "reevaluate_entity({0}, {1}) failed. Return code: {2}",
        4028: PREFIX + "reevaluate_record({0}, {1}, {2}) failed. Return code: {3}",
        4029: PREFIX + "reinitialize({0}) failed. Return code: {1}",
        4030: PREFIX + "search_by_attributes({0}) failed. Return code: {1}",
        4031: PREFIX + "why_entities({0}, {1}) failed. Return code: {2}",
        4032: PREFIX + "why_records({0}, {1}, {2}, {3}, {4}) failed. Return code: {5}",
        4033: PREFIX + "why_record_in_entity{0}, {1}, {2}) failed. Return code: {3}",
        4034: (
            PREFIX
            + "SzEngine({0}, {1}) failed. instance_name and settings must both be set or"
            " both be empty"
        ),
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
        record_definition: Union[str, Dict[Any, Any]],
        flags: int = 0,
        **kwargs: Any,
    ) -> str:
        """
        The `add_record` method adds a record into the Senzing repository.
        Can be called as many times as desired and from multiple threads at the same time.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            record_definition (str | Dict): A JSON document containing the record to be added to the Senzing repository.
            flags (int, optional): Flags used to control information returned. Defaults to 0.

        Returns:
            str: If flags are set to return the WITH_INFO response a JSON document containing the details, otherwise an empty JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/add_record.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def close_export(self, export_handle: int, **kwargs: Any) -> None:
        """
        The `close_export` method closes the exported document created by `export_json_entity_report`.
        It is part of the `export_json_entity_report`, `fetch_next`, `close_export`
        lifecycle of a list of sized entities.

        Args:
            export_handle (int): A handle created by `export_json_entity_report` or `export_csv_entity_report`.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/export_json_fetch_close.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/export_json_fetch_close.txt
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

            .. literalinclude:: ../../examples/szengine/count_redo_records.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def delete_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = 0,
        **kwargs: Any,
    ) -> str:
        """
        The `delete_record` method deletes a record from the Senzing repository.
        Can be called as many times as desired and from multiple threads at the same time.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            load_id (str, optional): An identifier used to distinguish different load batches/sessions. An empty string is acceptable. Defaults to "".
            flags (int, optional): Flags used to control information returned. Defaults to 0.

        Returns:
            str: If flags are set to return the WITH_INFO response a JSON document containing the details, otherwise an empty JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/delete_record.py
                :linenos:
        """

    @abstractmethod
    def destroy(self, **kwargs: Any) -> None:
        """
        The `destroy` method releases resources and performs cleanup for the SzEngine object and any in-memory configurations.
        It should be called after all other calls are complete.

        **Note:** If the `SzEngine` constructor was called with parameters,
        the destructor will automatically call the destroy() method.
        In this case, a separate call to `destroy()` is not needed.

        Example:

        .. code-block:: python

            sz_engine = szengine.SzEngine(instance_name, settings)

        Raises:
            szexception.SzError:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/szengine_init_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def export_csv_entity_report(
        self,
        csv_column_list: str,
        flags: int = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> int:
        # TODO Add into docstring a good default csv_column_list example
        """
        **Warning:** `export_csv_entity_report` is not recommended for large systems as it does not scale.
        It is recommended larger systems implement real-time replication to a data warehouse.

        The `export_csv_entity_report` method initializes a cursor over a document of exported entities.
        It is part of the `export_csv_entity_report`, `fetch_next`, `close_export`
        lifecycle of a list of entities to export.

        Args:
            csv_column_list (str): A comma-separated list of column names for the CSV export.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS.

        Returns:
            int: A handle that identifies the document to be scrolled through using `fetch_next`.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/export_csv_fetch_close.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/export_csv_fetch_close.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def export_json_entity_report(
        self, flags: int = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS, **kwargs: Any
    ) -> int:
        """
        **Warning:** `export_json_entity_report` is not recommended for large systems as it does not scale.
        It is recommended larger systems implement real-time replication to a data warehouse.

        The `export_json_entity_report` method initializes a cursor over a document of exported entities.
        It is part of the `export_json_entity_report`, `fetch_next`, `close_export`
        lifecycle of a list of entities to export.

        Args:
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS.

        Returns:
            int: A handle that identifies the document to be scrolled through using `fetch_next`.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/export_json_fetch_close.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/export_json_fetch_close.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def fetch_next(self, export_handle: int, **kwargs: Any) -> str:
        """
        The `fetch_next` method is used to scroll through an exported document one entity at a time.
        Successive calls of `fetch_next` will export successive rows of entity data until there is no more.
        It is part of the `export_json_entity_report` or `export_json_entity_report`, `fetch_next`, `close_export`
        lifecycle of a list of exported entities.

        Args:
            response_handle (int): A handle created by `export_json_entity_report` or `export_json_entity_report`.

        Returns:
            str: TODO:

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/export_json_fetch_close.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/export_json_fetch_close.txt
                :linenos:
                :language: json
        """

    # NOTE Included but not to be documented or examples, early adaptor feature, needs manual additions to config
    @abstractmethod
    def find_interesting_entities_by_entity_id(
        self, entity_id: int, flags: int = 0, **kwargs: Any
    ) -> str:
        """"""

    # NOTE Included but not to be documented or examples, early adaptor feature, needs manual additions to config
    @abstractmethod
    def find_interesting_entities_by_record_id(
        self, data_source_code: str, record_id: str, flags: int = 0, **kwargs: Any
    ) -> str:
        """"""

    @abstractmethod
    def find_network_by_entity_id(
        self,
        entity_list: Union[str, Dict[str, List[Dict[str, int]]]],
        max_degrees: int,
        build_out_degree: int,
        max_entities: int,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """
        The `find_network_by_entity_id` method finds all entities surrounding a requested set of entities.
        This includes the requested entities, paths between them, and relations to other nearby entities.
        Returns a JSON document that identifies the path between the each set of search entities (if the path exists),
        and the information for the entities in the path.

        Args:
            entity_list (str): A JSON document listing entities.
            max_degrees (int): The maximum number of degrees in paths between search entities.
            build_out_degree (int): The number of degrees of relationships to show around each search entity.
            max_entities (int): The maximum number of entities to return in the discovered network.
            flags (int, optional): The maximum number of entities to return in the discovered network. Defaults to SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/find_network_by_entity_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/find_network_by_entity_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def find_network_by_record_id(
        self,
        record_list: Union[str, Dict[str, List[Dict[str, str]]]],
        max_degrees: int,
        build_out_degree: int,
        max_entities: int,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """
        The `find_network_by_record_id` method finds all entities surrounding a requested set of entities by their RECORD_ID values.
        This includes the requested entities, paths between them, and relations to other nearby entities.
        Returns a JSON document that identifies the path between the each set of search entities (if the path exists),
        and the information for the entities in the path.

        Args:
            record_list (str): A JSON document listing records.
            max_degrees (int): The maximum number of degrees in paths between search entities.
            build_out_degree (int): The number of degrees of relationships to show around each search entity.
            max_entities (int): The maximum number of entities to return in the discovered network.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/find_network_by_record_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/find_network_by_record_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def find_path_by_entity_id(
        self,
        start_entity_id: int,
        end_entity_id: int,
        max_degrees: int,
        # TODO Should accept both entity and record IDs in V4, test
        exclusions: Union[str, Dict[Any, Any]] = "",
        required_data_sources: Union[str, Dict[Any, Any]] = "",
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """
        The `find_path_by_entity_id` method finds the most efficient relationship between two entities path based on the parameters
        and returns a JSON document with an ENTITY_PATHS section that details the path between the entities.
        The ENTITIES sections details information on the entities. Paths are found using known relationships with other entities.
        Paths are found using known relationships with other entities.

        Args:
            start_entity_id (int): The entity ID for the starting entity of the search path.
            end_entity_id (int): The entity ID for the ending entity of the search path.
            max_degrees (int): The maximum number of degrees in paths between search entities.
            exclusions (str): TODO
            required_data_sources (str): TODO
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS.

        Returns:
            str: A JSON document with an ENTITY_PATHS section that details the path between the entities.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/find_path_by_entity_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/find_path_by_entity_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def find_path_by_record_id(
        self,
        start_data_source_code: str,
        start_record_id: str,
        end_data_source_code: str,
        end_record_id: str,
        max_degrees: int,
        exclusions: Union[str, Dict[Any, Any]] = "",
        required_data_sources: Union[str, Dict[Any, Any]] = "",
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """
        The `find_path_by_record_id` method finds the most efficient relationship between
        two entities path based on the parameters by RECORD_ID values
        and returns a JSON document with an ENTITY_PATHS section that details the path between the entities.
        The ENTITIES sections details information on the entities.
        Paths are found using known relationships with other entities.
        The entities are identified by starting and ending records.

        Args:
            start_data_source_code (str): Identifies the provenance of the record for the starting entity of the search path.
            start_record_id (str): The unique identifier within the records of the same data source for the starting entity of the search path.
            end_data_source_code (str): Identifies the provenance of the record for the ending entity of the search path.
            end_record_id (str): The unique identifier within the records of the same data source for the ending entity of the search path.
            max_degrees (int): The maximum number of degrees in paths between search entities.
            exclusions (str): TODO
            required_data_sources (str): TODO
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/find_path_by_record_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/find_path_by_record_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_active_config_id(self, **kwargs: Any) -> int:
        """
        The `get_active_config_id` method returns the identifier of the currently active Senzing engine configuration.

        Returns:
            int: The identifier of the active Senzing Engine configuration.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_active_config_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_active_config_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """
        The `get_entity_by_entity_id` method returns entity data based on the ID of a resolved identity.

        Args:
            entity_id (int): The unique identifier of an entity.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_entity_by_entity_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_entity_by_entity_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_entity_by_record_id(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """
        The `get_entity_by_record_id` method returns entity data based on the ID of a record which is a member of the entity.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_entity_by_record_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_entity_by_record_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """
        The `get_record` method returns a JSON document of a single record from the Senzing repository.
        Can be called as many times as desired and from multiple threads at the same time.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS.

        Returns:
            str: A JSON document of a single record.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_record.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_record.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_redo_record(self, **kwargs: Any) -> str:
        """
        The `get_redo_record` method returns the next internally queued redo record from the Senzing repository.
        Usually, the `process_redo_record` or `process_redo_record_with_info` method is called to process the redo record
        retrieved by `get_redo_record`.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_redo_record.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_redo_record.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_repository_last_modified_time(self, **kwargs: Any) -> int:
        """
        The `get_repository_last_modified_time` method retrieves the last modified time of the Senzing repository,
        measured in the number of seconds between the last modified time and January 1, 1970 12:00am GMT (epoch time).

        Returns:
            int: A Unix Timestamp.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_repository_last_modified_time.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_repository_last_modified_time.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_stats(self, **kwargs: Any) -> str:
        """
        The `get_stats` method retrieves workload statistics for the current process.
        These statistics will automatically reset after retrieval.

        Returns:
            str:  A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/stats.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/stats.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_virtual_entity_by_record_id(
        self,
        record_list: Union[str, Dict[Any, Any]],
        flags: int = SzEngineFlags.SZ_VIRTUAL_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """
        The `get_virtual_entity_by_record_id` method creates a view of a virtual entity
        using a list of existing loaded records.
        The virtual entity is composed of only those records and their features.
        Entity resolution is not performed.

        Args:
            record_list (str): A JSON document of one or more records by DATA_SOURCE and RECORD_ID pairs, formatted as `{"RECORDS":[{"DATA_SOURCE":"DS1","RECORD_ID":"R1"},{"DATA_SOURCE":"DS2","RECORD_ID":"R2"}]}`.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_HOW_ENTITY_DEFAULT_FLAGS.

        Returns:
            str:  A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/get_virtual_entity_by_record_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/get_virtual_entity_by_record_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def how_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_HOW_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """
        The `how_entity_by_entity_id` method determines and details steps-by-step *how* records resolved to an ENTITY_ID.

        In most cases, *how* provides more detailed information than *why* as the resolution is detailed step-by-step.

        Args:
            entity_id (int): The unique identifier of an entity.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_HOW_ENTITY_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/how_entity_by_entity_id.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/how_entity_by_entity_id.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        config_id: Optional[int] = None,
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        # TODO docstring plugin
        """
        he ``initialize`` method initializes the Senzing SzEngine object.
        It must be called prior to any other calls.

        **Note:** If the SzEngine constructor is called with parameters,
        the constructor will automatically call the ``initialize()`` method.
        In this case, a separate call to ``initialize()`` is not needed.

        Example:

        .. code-block:: python

            sz_engine = szengine.SzEngine(instance_name, settings)

        Args:
            instance_name (str): A short name given to this instance of the SzEngine object, to help identify it within system logs.
            settings (str): A JSON string containing configuration parameters.
            config_id (int):
            verbose_logging (int): `Optional:` A flag to enable deeper logging of the Senzing processing. 0 for no Senzing logging; 1 for logging. Default: 0

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/szengine_init_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def prime_engine(self, **kwargs: Any) -> None:
        """
        The `prime_engine` method initializes high resource consumption components of Senzing
        used in some functions. If this call is not made, these resources are initialized the
        first time they are needed and can cause unusually long processing times the first time
        a function is called that requires these resources.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/prime_engine.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def process_redo_record(self, redo_record: str, flags: int, **kwargs: Any) -> str:
        """
        #TODO The `process_redo_record` method...

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/prime_engine.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def reevaluate_entity(self, entity_id: int, flags: int = 0, **kwargs: Any) -> str:
        """
        The `reevaluate_entity` method reevaluates the specified entity.

        Args:
            entity_id (int): The unique identifier of an entity.
            flags (int, optional): Flags used to control information returned. Defaults to 0.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/reevaluate_entity.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def reevaluate_record(
        self, data_source_code: str, record_id: str, flags: int = 0, **kwargs: Any
    ) -> str:
        """
        The `reevaluate_record` method reevaluates a specific record.

        Args:
            data_source_code (str): Identifies the provenance of the data.
            record_id (str): The unique identifier within the records of the same data source.
            flags (int, optional):  Flags used to control information returned. Defaults to 0.

        Returns:
            str: If flags are set to return the WITH_INFO response a JSON document containing the details, otherwise an empty JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/reevaluate_entity.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def reinitialize(self, config_id: int, **kwargs: Any) -> None:
        """
        The `reinitialize` method reinitializes the Senzing SzEngine object using a specific configuration
        identifier. A list of available configuration identifiers can be retrieved using
        `szconfigmgr.get_config_list`.

        Args:
            config_id (int): The configuration ID used for the initialization

        Raises:
            TypeError: Incorrect datatype of input parameter.
            szexception.SzError: config_id does not exist.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/szengine_reinit.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def search_by_attributes(
        self,
        attributes: Union[str, Dict[Any, Any]],
        search_profile: str = "",
        flags: int = SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """
        The `search_by_attributes` method retrieves entity data based on a user-specified set of entity attributes.

        Args:
            attributes (str):  A JSON document with the attribute data to search for.
            search_profile (str): The name of a configured search profile. Defaults to SEARCH.
            flags (int, optional): _description_. Defaults to SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/search_by_attributes.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/search_by_attributes.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def why_entities(
        self,
        entity_id_1: int,
        entity_id_2: int,
        flags: int = SzEngineFlags.SZ_WHY_ENTITIES_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """
        The `why_entities` method determines why entities did not resolve or why they do relate.

        Args:
            entity_id_1 (int): The entity ID for the starting entity of the search path.
            entity_id_2 (int): The entity ID for the ending entity of the search path.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_WHY_ENTITY_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/why_entities.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szengine/why_entities.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def why_records(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        flags: int = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """
        The `why_records` determines if any two records can or cannot resolve together, or if they relate.

        Args:
            data_source_code_1 (str): Identifies the provenance of the data.
            record_id_1 (str): The unique identifier within the records of the same data source.
            data_source_code_2 (str): Identifies the provenance of the data.
            record_id_2 (str): The unique identifier within the records of the same data source.
            flags (int, optional): Flags used to control information returned. Defaults to SzEngineFlags.SZ_WHY_ENTITY_DEFAULT_FLAGS.

        Returns:
            str: A JSON document.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szengine/why_records.py
                :linenos:
                :language: python

            **Output:**

        .. literalinclude:: ../../examples/szengine/why_records.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def why_record_in_entity(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        """ """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------

    # TODO doc strings for all return_dict methods it _return_dict methods are staying?
    def add_record_return_dict(
        self,
        data_source_code: str,
        record_id: str,
        record_definition: Union[str, Dict[Any, Any]],
        flags: int = 0,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """ """
        return cast(
            Dict[str, Any],
            # TODO orjson?
            json.loads(
                self.add_record(
                    data_source_code, record_id, record_definition, flags, **kwargs
                )
            ),
        )

    def delete_record_return_dict(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = 0,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        return cast(
            Dict[str, Any],
            json.loads(
                self.delete_record(data_source_code, record_id, flags, **kwargs)
            ),
        )

    def find_interesting_entities_by_entity_id_return_dict(
        self, entity_id: int, flags: int = 0, **kwargs: Any
    ) -> Dict[str, Any]:
        """ """
        return cast(
            Dict[str, Any],
            json.loads(
                self.find_interesting_entities_by_entity_id(entity_id, flags, **kwargs)
            ),
        )

    def find_interesting_entities_by_record_id_return_dict(
        self, data_source_code: str, record_id: str, flags: int = 0, **kwargs: Any
    ) -> Dict[str, Any]:
        """T"""
        return cast(
            Dict[str, Any],
            json.loads(
                self.find_interesting_entities_by_record_id(
                    data_source_code, record_id, flags, **kwargs
                )
            ),
        )

    def find_network_by_entity_id_return_dict(
        self,
        entity_list: Union[str, Dict[Any, Any]],
        max_degrees: int,
        build_out_degree: int,
        max_entities: int,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: document"""
        return cast(
            Dict[str, Any],
            json.loads(
                self.find_network_by_entity_id(
                    entity_list,
                    max_degrees,
                    build_out_degree,
                    max_entities,
                    flags,
                    **kwargs,
                )
            ),
        )

    def find_network_by_record_id_return_dict(
        self,
        record_list: Union[str, Dict[Any, Any]],
        max_degrees: int,
        build_out_degree: int,
        max_entities: int,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: document"""
        return cast(
            Dict[str, Any],
            json.loads(
                self.find_network_by_record_id(
                    record_list,
                    max_degrees,
                    build_out_degree,
                    max_entities,
                    flags,
                    **kwargs,
                )
            ),
        )

    def find_path_by_entity_id_return_dict(
        self,
        start_entity_id: int,
        end_entity_id: int,
        max_degrees: int,
        exclusions: Union[str, Dict[Any, Any]] = "",
        required_data_sources: Union[str, Dict[Any, Any]] = "",
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: document"""
        return cast(
            Dict[str, Any],
            json.loads(
                self.find_path_by_entity_id(
                    start_entity_id,
                    end_entity_id,
                    max_degrees,
                    exclusions,
                    required_data_sources,
                    flags,
                    **kwargs,
                )
            ),
        )

    def find_path_by_record_id_return_dict(
        self,
        start_data_source_code: str,
        start_record_id: str,
        end_data_source_code: str,
        end_record_id: str,
        max_degrees: int,
        exclusions: Union[str, Dict[Any, Any]] = "",
        required_data_sources: Union[str, Dict[Any, Any]] = "",
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """ """
        return cast(
            Dict[str, Any],
            json.loads(
                self.find_path_by_record_id(
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
            ),
        )

    def get_entity_by_entity_id_return_dict(
        self,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """ """
        return cast(
            Dict[str, Any],
            json.loads(self.get_entity_by_entity_id(entity_id, flags, **kwargs)),
        )

    def get_entity_by_record_id_return_dict(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """ """
        return cast(
            Dict[str, Any],
            json.loads(
                self.get_entity_by_record_id(
                    data_source_code, record_id, flags, **kwargs
                )
            ),
        )

    def get_record_return_dict(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """ """
        return cast(
            Dict[str, Any],
            json.loads(self.get_record(data_source_code, record_id, flags, **kwargs)),
        )

    def get_stats_return_dict(self, **kwargs: Any) -> Dict[str, Any]:
        return cast(
            Dict[str, Any],
            json.loads(self.get_stats(**kwargs)),
        )

    def get_virtual_entity_by_record_id_return_dict(
        self,
        record_list: Union[str, Dict[Any, Any]],
        flags: int = SzEngineFlags.SZ_VIRTUAL_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """ """
        return cast(
            Dict[str, Any],
            json.loads(
                self.get_virtual_entity_by_record_id(record_list, flags, **kwargs)
            ),
        )

    def how_entity_by_entity_id_return_dict(
        self,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_HOW_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """ """
        return cast(
            Dict[str, Any],
            json.loads(self.how_entity_by_entity_id(entity_id, flags, **kwargs)),
        )

    def reevaluate_entity_return_dict(
        self,
        entity_id: int,
        flags: int = 0,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """ """
        return cast(
            Dict[str, Any],
            json.loads(self.reevaluate_entity(entity_id, flags, **kwargs)),
        )

    def reevaluate_record_return_dict(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = 0,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """ """
        return cast(
            Dict[str, Any],
            json.loads(
                self.reevaluate_record(data_source_code, record_id, flags, **kwargs)
            ),
        )

    def search_by_attributes_return_dict(
        self,
        attributes: Union[str, Dict[Any, Any]],
        search_profile: str = "SEARCH",
        flags: int = SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """ """
        return cast(
            Dict[str, Any],
            json.loads(
                self.search_by_attributes(attributes, search_profile, flags, **kwargs)
            ),
        )

    def why_entities_return_dict(
        self,
        entity_id_1: int,
        entity_id_2: int,
        flags: int = SzEngineFlags.SZ_WHY_ENTITIES_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        return cast(
            Dict[str, Any],
            json.loads(self.why_entities(entity_id_1, entity_id_2, flags, **kwargs)),
        )

    def why_records_return_dict(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        flags: int = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        return cast(
            Dict[str, Any],
            json.loads(
                self.why_records(
                    data_source_code_1,
                    record_id_1,
                    data_source_code_2,
                    record_id_2,
                    flags,
                    **kwargs,
                )
            ),
        )

    def why_record_in_entity_return_dict(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """ """
        # TODO Is the cast needed?
        return cast(
            Dict[str, Any],
            json.loads(
                self.why_record_in_entity(data_source_code, record_id, flags, **kwargs)
            ),
        )
