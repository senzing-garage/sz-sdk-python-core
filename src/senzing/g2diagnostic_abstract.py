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
        # TODO: remove + concats for f-strings
        4001: PREFIX + "G2Diagnostic_checkDBPerf({0}) failed. Return code: {1}",
        4003: PREFIX + "G2Diagnostic_destroy() failed.  Return code: {0}",
        4007: PREFIX + "G2Diagnostic_getDBInfo() failed. Return code: {0}",
        4018: PREFIX + "G2Diagnostic_init({0}, {1}, {2}) failed. Return code: {3}",
        4019: PREFIX
        + "G2Diagnostic_initWithConfigID({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4020: PREFIX + "G2Diagnostic_reinit({0}) failed. Return Code: {1}",
        4021: PREFIX
        + "G2Config({0}, {1}) must have both module_name and ini_params nor neither.",
    }

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def check_db_perf(self, seconds_to_run: int, *args: Any, **kwargs: Any) -> str:
        """
        The `check_db_perf` method performs inserts to determine rate of insertion.

        Args:
            seconds_to_run (int): Duration of the test in seconds.

        Returns:
            str: A string containing a JSON document.

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic/check_db_perf.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2diagnostic/check_db_perf.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def destroy(self, *args: Any, **kwargs: Any) -> None:
        """
        The `destroy` method will destroy and perform cleanup for the Senzing G2Diagnostic object.
        It should be called after all other calls are complete.

        **Note:** If the `G2Diagnostic` constructor was called with parameters,
        the destructor will automatically call the destroy() method.
        In this case, a separate call to `destroy()` is not needed.

        Example:

        .. code-block:: python

            g2_diagnostic = g2diagnostic.G2Diagnostic(module_name, ini_params)

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic/g2diagnostic_init_and_destroy.py
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
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic/get_available_memory.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def get_db_info(self, *args: Any, **kwargs: Any) -> str:
        """
        The `get_db_info` method returns information about the database connection.

        Returns:
            str: A JSON document enumerating data sources.

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic/get_db_info.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2diagnostic/get_db_info.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_logical_cores(self, *args: Any, **kwargs: Any) -> int:
        """
        The `get_logical_cores` method returns the number of logical cores on the host system.

        Returns:
            int: Number of logical cores.

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic/get_logical_cores.py
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
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic/get_physical_cores.py
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
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic/get_total_system_memory.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def init(
        self, module_name: str, ini_params: str, verbose_logging: int = 0, **kwargs: Any
    ) -> None:
        """
        The `init` method initializes the Senzing G2Diagnosis object.
        It must be called prior to any other calls.

        **Note:** If the G2Diagnosis constructor is called with parameters,
        the constructor will automatically call the `init()` method.
        In this case, a separate call to `init()` is not needed.

        Example:

        .. code-block:: python

            g2_diagnosis = g2diagnosis.G2Diagnosis(module_name, ini_params)

        Args:
            module_name (str): A name for the auditing node, to help identify it within system logs.
            ini_params (str): A JSON string containing configuration parameters.
            verbose_logging (int): `Optional:` A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging. Default: 0

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic/g2diagnostic_init_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def init_with_config_id(
        self,
        module_name: str,
        ini_params: str,
        init_config_id: int,
        verbose_logging: int = 0,
        **kwargs: Any
    ) -> None:
        """
        The `init_with_config_id` method initializes the Senzing G2Diagnosis object with a non-default configuration ID.
        It must be called prior to any other calls.

        **Note:** If the G2Diagnosis constructor is called with parameters,
        the constructor will automatically call the `init()` method.
        In this case, a separate call to `init()` is not needed.

        Example:

        .. code-block:: python

            g2_diagnosis = g2diagnosis.G2Diagnosis(module_name, ini_params, init_config_id)

        Args:
            module_name (str): A name for the auditing node, to help identify it within system logs.
            ini_params (str): A JSON string containing configuration parameters.
            init_config_id (int): The configuration ID used for the initialization.
            verbose_logging (int): `Optional:` A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging. Default: 0

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic/init_with_config_id.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def reinit(self, init_config_id: int, *args: Any, **kwargs: Any) -> None:
        """
        The `reinit` method re-initializes the Senzing G2Diagnosis object.

        Args:
            init_config_id (int): The configuration ID used for the initialization

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic/reinit.py
                :linenos:
                :language: python
        """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
