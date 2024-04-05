#! /usr/bin/env python3

"""
TODO: g2diagnostic_abstract.py
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

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
        # TODO: remove + concats for f-strings?
        4001: PREFIX + "G2Diagnostic_checkDBPerf({0}) failed. Return code: {1}",
        4003: PREFIX + "G2Diagnostic_destroy() failed.  Return code: {0}",
        4007: PREFIX + "G2Diagnostic_getDBInfo() failed. Return code: {0}",
        4018: PREFIX + "G2Diagnostic_init({0}, {1}, {2}) failed. Return code: {3}",
        4019: PREFIX
        + "G2Diagnostic_initWithConfigID({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4020: PREFIX + "G2Diagnostic_reinit({0}) failed. Return Code: {1}",
        4021: PREFIX
        + "G2Config({0}, {1}) must have both module_name and ini_params nor neither.",
        # TODO What style for the API name?
        # TODO Reorder
        4023: PREFIX + "G2_purgeRepository() failed. Return code: {0}",
    }

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def check_database_performance(
        self, seconds_to_run: int, *args: Any, **kwargs: Any
    ) -> str:
        """
        The `check_database_performance` method performs inserts to determine rate of insertion.

        Args:
            seconds_to_run (int): Duration of the test in seconds.

        Returns:
            str: A string containing a JSON document.

        Raises:
            TypeError: Incorrect datatype of input parameter.
            g2exception.G2Exception:

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
            g2exception.G2Exception:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic/g2diagnostic_init_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def initialize(
        self,
        instance_name: str,
        settings: str | Dict[Any, Any],
        verbose_logging: int = 0,
        **kwargs: Any
    ) -> None:
        """
        The `initialize` method initializes the Senzing G2Diagnosis object.
        It must be called prior to any other calls.

        **Note:** If the G2Diagnosis constructor is called with parameters,
        the constructor will automatically call the `initialize()` method.
        In this case, a separate call to `initialize()` is not needed.

        Example:

        .. code-block:: python

            g2_diagnosis = g2diagnosis.G2Diagnosis(module_name, ini_params)

        Args:
            instance_name (str): A name for the auditing node, to help identify it within system logs.
            settings (Union[str, Dict[Any, Any]]): A JSON string containing configuration parameters.
            verbose_logging (int): `Optional:` A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging. Default: 0

        Raises:
            TypeError: Incorrect datatype of input parameter.
            g2exception.G2Exception:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic/g2diagnostic_init_and_destroy.py
                :linenos:
                :language: python
        """

    # @abstractmethod
    # def init_with_config_id(
    #     self,
    #     module_name: str,
    #     ini_params: Union[str, Dict[Any, Any]],
    #     init_config_id: int,
    #     verbose_logging: int = 0,
    #     **kwargs: Any
    # ) -> None:
    #     """
    #     The `init_with_config_id` method initializes the Senzing G2Diagnosis object with a non-default configuration ID.
    #     It must be called prior to any other calls.

    #     **Note:** If the G2Diagnosis constructor is called with parameters,
    #     the constructor will automatically call the `init()` method.
    #     In this case, a separate call to `init()` is not needed.

    #     Example:

    #     .. code-block:: python

    #         g2_diagnosis = g2diagnosis.G2Diagnosis(module_name, ini_params, init_config_id)

    #     Args:
    #         module_name (str): A name for the auditing node, to help identify it within system logs.
    #         ini_params Union[str, Dict[Any, Any]]): A JSON string containing configuration parameters.
    #         init_config_id (int): The configuration ID used for the initialization.
    #         verbose_logging (int): `Optional:` A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging. Default: 0

    #     Raises:
    #         TypeError: Incorrect datatype of input parameter.
    #         g2exception.G2Exception:

    #     .. collapse:: Example:

    #         .. literalinclude:: ../../examples/g2diagnostic/g2diagnostic_init_with_config_id.py
    #             :linenos:
    #             :language: python
    #     """

    @abstractmethod
    def purge_repository(self, **kwargs: Any) -> None:
        """
        **Warning:**
        The `purge_repository` method removes every record in the Senzing repository.

        Before calling `purge_repository` all other instances of the Senzing API
        MUST be destroyed or shutdown.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic/purge_repository.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def reinitialize(self, config_id: int, *args: Any, **kwargs: Any) -> None:
        """
        The `reinitialize` method re-initializes the Senzing G2Diagnosis object.

        Args:
            config_id (int): The configuration ID used for the initialization

        Raises:
            TypeError: Incorrect datatype of input parameter.
            g2exception.G2Exception: init_config_id does not exist.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2diagnostic/g2diagnostic_reinit.py
                :linenos:
                :language: python
        """
