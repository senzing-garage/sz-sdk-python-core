"""
szproduct_abstract.py is the abstract class for all implementations of szproduct.
"""

# TODO: Determine specific SzError, Errors for "Raises:" documentation.
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Union, cast

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
    def destroy(self, **kwargs: Any) -> None:
        """
        The `destroy` method will destroy and perform cleanup for the Senzing SzProduct object.
        It should be called after all other calls are complete.

        **Note:** If the `SzProduct` constructor was called with parameters,
        the destructor will automatically call the destroy() method.
        In this case, a separate call to `destroy()` is not needed.

        Raises:
            szexception.SzError:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szproduct/szproduct_initialize_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
        **kwargs: Any
    ) -> None:
        """
        The `initialize` method initializes the Senzing SzProduct object.
        It must be called prior to any other calls.

        **Note:** If the SzProduct constructor is called with parameters,
        the constructor will automatically call the `initialize()` method.
        In this case, a separate call to `initialize()` is not needed.

        Args:
            instance_name (str): A short name given to this instance of the SzProduct object, to help identify it within system logs.
            settings (str): A JSON string containing configuration parameters.
            verbose_logging (int): `Optional:` A flag to enable deeper logging of the Senzing processing. 0 for no Senzing logging; 1 for logging. Default: 0

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szproduct/szproduct_initialize_and_destroy.py
                :linenos:
                :language: python
        """

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

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------

    def license_as_dict(self, **kwargs: Any) -> Dict[str, Any]:
        """
        A convenience method for
        :meth:`senzing_abstract.SzProductAbstract.get_license`

        Returns:
            Dict[str, Any]: A dictionary containing Senzing license metadata.
        """
        return cast(
            Dict[str, Any],
            json.loads(self.get_license(**kwargs)),
        )

    def version_as_dict(self, **kwargs: Any) -> Dict[str, Any]:
        """
        A convenience method for
        :meth:`senzing_abstract.SzProductAbstract.get_version`

        Returns:
            Dict[str, Any]: A dictionary containing metadata about the Senzing Engine version being used.
        """
        return cast(
            Dict[str, Any],
            json.loads(self.get_version(**kwargs)),
        )
