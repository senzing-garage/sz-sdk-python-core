#! /usr/bin/env python3

"""
TODO: g2diagnostic_abstract.py
"""

from abc import ABC, abstractmethod
from typing import Any

# Metadata

__all__ = ["G2DiagnosticAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

# -----------------------------------------------------------------------------
# G2DiagnosticAbstract
# -----------------------------------------------------------------------------


class G2DiagnosticAbstract(ABC):
    """
    G2 diagnostic module access library
    """

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    PREFIX = "g2diagnostic."
    ID_MESSAGES = {
        4001: PREFIX + "G2Diagnostic_checkDBPerf({0}) failed. Return code: {1}",
        4002: PREFIX + "G2Diagnostic_closeEntityListBySize() failed. Return code: {0}",
        4003: PREFIX + "G2Diagnostic_destroy() failed.  Return code: {0}",
        4004: PREFIX + "G2Diagnostic_fetchNextEntityBySize() failed.  Return code: {0}",
        4005: PREFIX
        + "G2Diagnostic_findEntitiesByFeatureIDs({0}) failed. Return code: {1}",
        4006: PREFIX + "G2Diagnostic_getDataSourceCounts() failed. Return code: {0}",
        4007: PREFIX + "G2Diagnostic_getDBInfo() failed. Return code: {0}",
        4008: PREFIX
        + "G2Diagnostic_getEntityDetails({0}, {1}) failed. Return code: {2}",
        4009: PREFIX + "G2Diagnostic_getEntityListBySize({0}) failed. Return code: {1}",
        4010: PREFIX + "G2Diagnostic_getEntityResume({0}) failed. Return code: {1}",
        4011: PREFIX
        + "G2Diagnostic_getEntitySizeBreakdown({0}, {1}) failed. Return code: {2}",
        4012: PREFIX + "G2Diagnostic_getFeature({0}) failed. Return code: {1}",
        4013: PREFIX
        + "G2Diagnostic_getGenericFeatures({0}, {1}) failed. Return code: {2}",
        4014: PREFIX + "G2Diagnostic_getLastException() failed. Return code: {0}",
        4015: PREFIX
        + "G2Diagnostic_getMappingStatistics({0}) failed. Return code: {1}",
        4016: PREFIX
        + "G2Diagnostic_getRelationshipDetails({0}, {1}) failed. Return code: {2}",
        4017: PREFIX
        + "G2Diagnostic_getResolutionStatistics() failed. Return code: {0}",
        4018: PREFIX + "G2Diagnostic_init({0}, {1}, {2}) failed. Return code: {3}",
        4019: PREFIX
        + "G2Diagnostic_initWithConfigID({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4020: PREFIX + "G2Diagnostic_reinit({0}) failed. Return Code: {1}",
    }

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def check_db_perf(self, seconds_to_run: int, *args: Any, **kwargs: Any) -> str:
        """
        The `check_db_perf` method performs inserts to determine rate of insertion.

        Parameters:
            seconds_to_run: Duration of the test in seconds.

        Returns:
            str: A string containing a JSON document. Example: `{"numRecordsInserted":0,"insertTime":0}`

        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic_check_db_perf_test.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def destroy(self, *args: Any, **kwargs: Any) -> None:
        """
        The `check_db_perf` method performs inserts to determine rate of insertion.

        Parameters:
            seconds_to_run: Duration of the test in seconds.

        Returns:
            str: A string containing a JSON document. Example: `{"numRecordsInserted":0,"insertTime":0}`

        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic_check_db_perf_test.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def get_available_memory(self, *args: Any, **kwargs: Any) -> int:
        """
        The `get_available_memory` method returns the available memory, in bytes, on the host system.

        Returns:
            int: Number of bytes of available memory.

        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic_get_available_memory_test.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def get_db_info(self, *args: Any, **kwargs: Any) -> str:
        """
        The `get_db_info` method returns information about the database connection.

        Returns:
            str: A JSON document enumerating data sources. Example: `{"Hybrid Mode":false,"Database Details":[{"Name":"0.0.0.0","Type":"postgresql"}]}`

        Raises:
            None: No exceptions raised

        .. only:: bob_g2diagnostic
            .. collapse:: Examplea:

                .. literalinclude:: ../../examples/g2diagnostic_get_db_info_test.py
                    :linenos:
                    :language: python

        .. only:: bob_g2diagnostic_grpc
            .. collapse:: Exampleb:

                .. literalinclude:: ../../examples/g2diagnostic_grpc_get_db_info_test.py
                    :linenos:
                    :language: python
        """

    @abstractmethod
    def get_logical_cores(self, *args: Any, **kwargs: Any) -> int:
        """
        The `get_logical_cores` method returns the number of logical cores on the host system.

        Returns:
            int: Number of logical cores.

        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic_get_logical_cores_test.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def get_physical_cores(self, *args: Any, **kwargs: Any) -> int:
        """
        The `get_physical_cores` method returns the number of physical cores on the host system.

        Returns:
            int: Number of physical cores.

        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic_get_physical_cores_test.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def get_total_system_memory(self, *args: Any, **kwargs: Any) -> int:
        """
        The `get_total_system_memory` method returns the total memory, in bytes, on the host system.

        Returns:
            int: Number of bytes of memory.

        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic_get_total_system_memory_test.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def init(
        self,
        module_name: str,
        ini_params: str,
        verbose_logging: int,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        The `init` method initializes the Senzing G2Diagnosis object.
        It must be called prior to any other calls.

        Parameters:
            module_name:
                A name for the auditing node, to help identify it within system logs.
            ini_params:
                A JSON string containing configuration parameters.
            verbose_logging:
                A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic_init_test.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def init_with_config_id(
        self,
        module_name: str,
        ini_params: str,
        init_config_id: int,
        verbose_logging: int,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        The `init_with_config_id` method initializes the Senzing G2Diagnosis object with a non-default configuration ID.
        It must be called prior to any other calls.

        Parameters:
            module_name:
                A name for the auditing node, to help identify it within system logs.
            ini_params:
                A JSON string containing configuration parameters.
            init_config_id:
                The configuration ID used for the initialization.
            verbose_logging:
                A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging.

        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic_init_with_config_id_test.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def reinit(self, init_config_id: int, *args: Any, **kwargs: Any) -> None:
        """
        The `reinit` method re-initializes the Senzing G2Diagnosis object.

        Parameters:
            The configuration ID used for the initialization.

        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic_reinit_test.py
                :linenos:
                :language: python
        """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
