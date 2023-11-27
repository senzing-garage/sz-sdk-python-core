#! /usr/bin/env python3

"""
g2product_abstract.py is the abstract class for all implementaions of g2product.
"""

# TODO: Determine specific G2Exceptions, Errors for "Raises:" documentation.

import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Union, cast

# Metadata

__all__ = ["G2ProductAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-27"

# -----------------------------------------------------------------------------
# G2ProductAbstract
# -----------------------------------------------------------------------------


class G2ProductAbstract(ABC):
    """
    G2ProductAbstract is the definition of the Senzing Python API that is
    implemented by packages such as g2product.py.
    """

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    PREFIX = "g2product."
    ID_MESSAGES = {
        4001: PREFIX + "G2Product_destroy() failed. Return code: {0}",
        4002: PREFIX + "G2Product_init({0}, {1}, {2}) failed. Return code: {3}",
        4003: PREFIX
        + "G2Product({0}, {1}) failed. module_name and ini_params must both be set or both be empty",
    }

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def destroy(self, *args: Any, **kwargs: Any) -> None:
        """
        The `destroy` method will destroy and perform cleanup for the Senzing G2Product object.
        It should be called after all other calls are complete.

        **Note:** If the `G2Product` constructor was called with parameters,
        the destructor will automatically call the destroy() method.
        In this case, a separate call to `destroy()` is not needed.

        Example:

        .. code-block:: python

            g2_product = g2product.G2Product(module_name, ini_params)

        Raises:
            g2exception.G2Exception:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2product/g2product_init_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def init(
        self,
        module_name: str,
        ini_params: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
        **kwargs: Any
    ) -> None:
        """
        The `init` method initializes the Senzing G2Product object.
        It must be called prior to any other calls.

        **Note:** If the G2Product constructor is called with parameters,
        the constructor will automatically call the `init()` method.
        In this case, a separate call to `init()` is not needed.

        Example:

        .. code-block:: python

            g2_product = g2product.G2Product(module_name, ini_params)

        Args:
            module_name (str): A short name given to this instance of the G2Product object, to help identify it within system logs.
            ini_params (str): A JSON string containing configuration parameters.
            verbose_logging (int): `Optional:` A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging. Default: 0

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2product/g2product_init_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def license(self, *args: Any, **kwargs: Any) -> str:
        """
        .. _license:

        The `license` method retrieves information about the currently used license by the Senzing API.

        Returns:
            str: A JSON document containing Senzing license metadata.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2product/license.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2product/license.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def version(self, *args: Any, **kwargs: Any) -> str:
        """
        .. _version:

        The `version` method returns the version of the Senzing API.

        Returns:
            str: A JSON document containing metadata about the Senzing Engine version being used.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2product/version.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2product/version.txt
                :linenos:
                :language: json
        """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------

    def license_as_dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        A convenience method for
        :ref:`license<license>`.

        Returns:
            Dict[str, Any]: A dictionary containing Senzing license metadata.

        """
        return cast(
            Dict[str, Any],
            json.loads(self.license(args, kwargs)),
        )

    def version_as_dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        A convenience method for
        :ref:`version<version>`.

        Returns:
            Dict[str, Any]: A dictionary containing metadata about the Senzing Engine version being used.

        """
        return cast(
            Dict[str, Any],
            json.loads(self.version(args, kwargs)),
        )
