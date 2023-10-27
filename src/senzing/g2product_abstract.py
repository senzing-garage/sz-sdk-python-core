#! /usr/bin/env python3

"""
TODO: g2product_abstract.py
"""

from abc import ABC, abstractmethod
from typing import Any

# Metadata

__all__ = ["G2ProductAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

# -----------------------------------------------------------------------------
# G2ProductAbstract
# -----------------------------------------------------------------------------


class G2ProductAbstract(ABC):
    """
    G2 product module access library
    """

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    PREFIX = "g2product."
    ID_MESSAGES = {
        4001: PREFIX + "G2Product_destroy() failed. Return code: {0}",
        4002: PREFIX + "G2Product_getLastException() failed. Return code: {0}",
        4003: PREFIX + "G2Product_init({0}, {1}, {2}) failed. Return code: {3}",
    }

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def destroy(self, *args: Any, **kwargs: Any) -> None:
        """
        The Destroy method will destroy and perform cleanup for the Senzing G2Product object.
        It should be called after all other calls are complete.

        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2product_destroy.py
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
        The `init` method initializes the Senzing G2Product object.
        It must be called prior to any other calls.

        Parameters:
            module_name:
                A name for the auditing node, to help identify it within system logs.
            ini_params:
                A JSON string containing configuration parameters.
            verbose_logging:
                A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2product_init.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def license(self, *args: Any, **kwargs: Any) -> str:
        """
        The License method retrieves information about the currently used license by the Senzing API.

        Returns:
            str: A JSON document containing Senzing license metadata.

        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2product_license.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def version(self, *args: Any, **kwargs: Any) -> str:
        """
        The Version method returns the version of the Senzing API.

        Returns:
            str: A JSON document containing metadata about the Senzing Engine version being used.

        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2product_version.py
                :linenos:
                :language: python
        """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
