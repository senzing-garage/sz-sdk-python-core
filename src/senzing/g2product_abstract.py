#! /usr/bin/env python3

"""
TODO: g2product_abstract.py
"""

import json
from abc import ABC, abstractmethod
from typing import Any, Dict, cast

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
    G2ProductAbstract is the definition of the Senzing Python API that is
    implemented by packages such as g2product.py.
    """

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    PREFIX = "g2product."
    ID_MESSAGES = {
        4001: PREFIX + "G2Product_destroy() failed. Return code: {0}",
        4002: PREFIX + "G2Product_getLastException() failed. Return code: {0}",
        4003: PREFIX + "G2Product_init({0}, {1}, {2}) failed. Return code: {3}",
        4004: PREFIX
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

            g2_product = g2product.G2Product(MODULE_NAME, INI_PARAMS)


        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2product_init_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def init(
        self, module_name: str, ini_params: str, verbose_logging: int = 0, **kwargs: Any
    ) -> None:
        """
        The `init` method initializes the Senzing G2Product object.
        It must be called prior to any other calls.

        **Note:** If the G2Product constructor is called with parameters,
        the constructor will automatically call the `init()` method.
        In this case, a separate call to `init()` is not needed.

        Example:

        .. code-block:: python

            g2_product = g2product.G2Product(MODULE_NAME, INI_PARAMS)

        Args:
            module_name:
                A name for the auditing node, to help identify it within system logs.
            ini_params:
                A JSON string containing configuration parameters.
            verbose_logging:
                `Optional:` A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging. Default: 0

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2product_init_and_destroy.py
                :linenos:
                :language: python

        """

    @abstractmethod
    def license(self, *args: Any, **kwargs: Any) -> str:
        """
        The `license` method retrieves information about the currently used license by the Senzing API.

        Returns:
            str: A JSON document containing Senzing license metadata.

        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2product_license.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2product_license.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def version(self, *args: Any, **kwargs: Any) -> str:
        """
        The `version` method returns the version of the Senzing API.

        Returns:
            str: A JSON document containing metadata about the Senzing Engine version being used.

        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2product_version.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2product_version.txt
                :linenos:
                :language: json
        """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------

    def version_as_dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        A convenience method for
        :ref`version<version>`.

        Returns:
            Dict[str, Any]: A dictionary containing metadata about the Senzing Engine version being used.
        """
        return cast(
            Dict[str, Any],
            json.loads(self.version(args, kwargs)),
        )
