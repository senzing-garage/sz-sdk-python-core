#! /usr/bin/env python3

"""
TODO: szdiagnostic_abstract.py
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

# Metadata

__all__ = ["SzDiagnosticAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

# -----------------------------------------------------------------------------
# G2DiagnosticAbstract
# -----------------------------------------------------------------------------


class SzDiagnosticAbstract(ABC):
    """
    Senzing diagnostic module access library
    """

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    PREFIX = "szdiagnostic."
    ID_MESSAGES = {
        4001: PREFIX + "check_database_performance({0}) failed. Return code: {1}",
        4002: PREFIX + "destroy() failed. Return code: {0}",
        4003: PREFIX + "initialize({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4004: PREFIX + "purge_repository() failed. Return code: {0}",
        4005: PREFIX + "reinitialize({0}) failed. Return Code: {1}",
        4006: PREFIX
        + "SzDiagnostic({0}, {1}) must have both instance_name and ini_settings nor neither.",
    }

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def check_database_performance(self, seconds_to_run: int, **kwargs: Any) -> str:
        """
        The `check_database_performance` method performs inserts to determine rate of insertion.

        Args:
            seconds_to_run (int): Duration of the test in seconds.

        Returns:
            str: A string containing a JSON document.

        Raises:
            TypeError: Incorrect datatype of input parameter.
            szexception.SzException:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szdiagnostic/check_db_perf.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szdiagnostic/check_db_perf.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def destroy(self, **kwargs: Any) -> None:
        """
        The `destroy` method will destroy and perform cleanup for the Senzing SzDiagnostic object.
        It should be called after all other calls are complete.

        **Note:** If the `SzDiagnostic` constructor was called with parameters,
        the destructor will automatically call the destroy() method.
        In this case, a separate call to `destroy()` is not needed.

        Example:

        .. code-block:: python

            sz_diagnostic = szdiagnostic.SzDiagnostic(instance_name, settings)

        Raises:
            szexception.SzException:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szdiagnostic/szdiagnostic_init_and_destroy.py
                :linenos:
                :language: python
        """

    # TODO Complete when added to Go helpers - GDEV-3801
    # NOTE This is included but not to be documented
    # @abstractmethod
    # def get_feature(self, feature_id: int, **kwargs: Any) -> str:
    #     """"""

    @abstractmethod
    def initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        config_id: Optional[int] = None,
        verbose_logging: int = 0,
        **kwargs: Any
    ) -> None:
        # TODO Add in config_id to docstring
        """
        The `initialize` method initializes the Senzing SzDiagnosis object.
        It must be called prior to any other calls.

        **Note:** If the Sz Diagnosis constructor is called with parameters,
        the constructor will automatically call the `initialize()` method.
        In this case, a separate call to `initialize()` is not needed.

        Example:

        .. code-block:: python

            sz_diagnosis = szdiagnosis.SzDiagnosis(instance_name, settings)

        Args:
            instance_name (str): A name for the auditing node, to help identify it within system logs.
            settings (Union[str, Dict[Any, Any]]): A JSON string containing configuration parameters.
            config_id (int):
            verbose_logging (int): `Optional:` A flag to enable deeper logging of the Senzing processing. 0 for no Senzing logging; 1 for logging. Default: 0

        Raises:
            TypeError: Incorrect datatype of input parameter.
            szexception.SzException:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szdiagnostic/szdiagnostic_init_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def purge_repository(self, **kwargs: Any) -> None:
        """
        **Warning:**
        The `purge_repository` method removes every record in the Senzing repository.

        Before calling `purge_repository` all other instances of the Senzing API
        MUST be destroyed or shutdown.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szdiagnostic/purge_repository.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def reinitialize(self, config_id: int, **kwargs: Any) -> None:
        """
        The `reinitialize` method re-initializes the Senzing SzDiagnostic object.

        Args:
            config_id (int): The configuration ID used for the initialization

        Raises:
            TypeError: Incorrect datatype of input parameter.
            szexception.SzException: config_id does not exist.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/sziagnostic/szdiagnostic_reinit.py
                :linenos:
                :language: python
        """
