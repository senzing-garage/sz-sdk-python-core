#! /usr/bin/env python3

"""
TODO: szdiagnostic_abstract.py
"""

from abc import ABC, abstractmethod
from typing import Any

from .szhelpers import construct_help

# Metadata

__all__ = ["SzDiagnosticAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

# -----------------------------------------------------------------------------
# SzDiagnosticAbstract
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
        4001: PREFIX + "check_datastore_performance({0}) failed. Return code: {1}",
        4002: PREFIX + "destroy() failed. Return code: {0}",
        4003: PREFIX + "get_datastore_info() failed. Return code: {0}",
        4004: PREFIX + "get_feature({0}) failed. Return code: {1}",
        4005: PREFIX + "initialize({0}, {1}, {2}, {3}) failed. Return code: {4}",
        4006: PREFIX + "purge_repository() failed. Return code: {0}",
        4007: PREFIX + "reinitialize({0}) failed. Return Code: {1}",
        4008: PREFIX
        + "SzDiagnostic({0}, {1}) failed. instance_name and settings must both be set or both be empty",
    }

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def check_datastore_performance(self, seconds_to_run: int, **kwargs: Any) -> str:
        """
        The `check_datastore_performance` method performs inserts to determine rate of insertion.

        Args:
            seconds_to_run (int): Duration of the test in seconds.

        Returns:
            str: A string containing a JSON document.

        Raises:
            TypeError: Incorrect datatype of input parameter.
            szexception.SzError:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szdiagnostic/check_datastore_performance.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szdiagnostic/check_datastore_performance.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_datastore_info(self, **kwargs: Any) -> str:
        """
        TODO: Document get_datastore_info()
        The `get_datastore_info` method will...

        Raises:
            szexception.SzError:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szdiagnostic/get_datastore_info.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szdiagnostic/get_datastore_info.txt
                :linenos:
                :language: json
        """

    # NOTE This is included but not to be documented
    @abstractmethod
    def get_feature(self, feature_id: int, **kwargs: Any) -> str:
        """TODO:  Document get_feature()"""

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
            szexception.SzError: config_id does not exist.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szdiagnostic/szdiagnostic_reinitialize.py
                :linenos:
                :language: python
        """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------

    def help(self, method_name: str = "") -> str:
        """
        Return the help for a particular message.

        Args:
            method_name (str): The name of the method. (e.g. "init"). If empty, a list of methods and descriptions is returned.

        Returns:
            str: The Help information about the requested method
        """
        return construct_help(self, method_name=method_name)
