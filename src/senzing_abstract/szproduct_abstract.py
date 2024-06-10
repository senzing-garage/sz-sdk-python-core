"""
szproduct_abstract.py is the abstract class for all implementations of szproduct.
"""

# TODO: Determine specific SzError, Errors for "Raises:" documentation.
from abc import ABC, abstractmethod
from typing import Any

# Metadata

__all__ = ["SzProductAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-27"

# -----------------------------------------------------------------------------
# SzProductAbstract
# -----------------------------------------------------------------------------


class SzProductAbstract(ABC):
    """
    SzProductAbstract is the definition of the Senzing Python API that is
    implemented by packages such as szproduct.py.
    """

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def get_license(self, **kwargs: Any) -> str:
        """
        The `get_license` method retrieves information about the currently used license by the Senzing API.

        Returns:
            str: A JSON document containing Senzing license metadata.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szproduct/get_license.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szproduct/get_license.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_version(self, **kwargs: Any) -> str:
        """
        The `get_version` method returns the version of the Senzing API.

        Returns:
            str: A JSON document containing metadata about the Senzing Engine version being used.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szproduct/get_version.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szproduct/get_version.txt
                :linenos:
                :language: json
        """
