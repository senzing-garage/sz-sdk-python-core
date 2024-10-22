#! /usr/bin/env python3

"""
szabstractfactory_abstract.py is the abstract class for all implementations of szabstractfactory.
"""


from abc import ABC, abstractmethod
from typing import Any

from .szconfig_abstract import SzConfigAbstract
from .szconfigmanager_abstract import SzConfigManagerAbstract
from .szdiagnostic_abstract import SzDiagnosticAbstract
from .szengine_abstract import SzEngineAbstract
from .szhelpers import construct_help
from .szproduct_abstract import SzProductAbstract

# Metadata

__all__ = ["SzAbstractFactoryAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2024-09-23"
__updated__ = "2024-09-23"

# -----------------------------------------------------------------------------
# SzAbstractFactoryAbstract
# -----------------------------------------------------------------------------


class SzAbstractFactoryAbstract(ABC):
    """
    SzAbstractFactoryAbstract is the definition of the Senzing Python API
    SzAbstractFactory implementations.
    """

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def create_sz_config(self) -> SzConfigAbstract:
        """
        The `create_sz_config` method creates a new implementation of an `SzConfigAbstract` object.

        Args:

        Returns:
            SzConfigAbstract: A new implementation.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szabstractfactory/create_sz_config.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szabstractfactory/create_sz_config.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def create_sz_configmanager(self) -> SzConfigManagerAbstract:
        """
        The `create_sz_configmanager` method creates a new implementation of an `SzConfigManagerAbstract` object.

        Args:

        Returns:
            SzConfigManagerAbstract: A new implementation.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szabstractfactory/create_sz_configmanager.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szabstractfactory/create_sz_configmanager.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def create_sz_diagnostic(self) -> SzDiagnosticAbstract:
        """
        The `create_sz_diagnostic` method creates a new implementation of an `SzDiagnosticAbstract` object.

        Args:

        Returns:
            SzDiagnosticAbstract: A new implementation.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szabstractfactory/create_sz_diagnostic.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szabstractfactory/create_sz_diagnostic.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def create_sz_engine(self) -> SzEngineAbstract:
        """
        The `create_sz_engine` method creates a new implementation of an `SzEngineAbstract` object.

        Args:

        Returns:
            SzEngineAbstract: A new implementation.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szabstractfactory/create_sz_engine.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szabstractfactory/create_sz_engine.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def create_sz_product(self) -> SzProductAbstract:
        """
        The `create_sz_product` method creates a new implementation of an `SzProductAbstract` object.

        Args:

        Returns:
            SzProductAbstract: A new implementation.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szabstractfactory/create_sz_product.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szabstractfactory/create_sz_product.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def destroy(self) -> None:
        """
        The `destroy` method ...FIXME: .

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szabstractfactory/destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def reinitialize(self, config_id: int, **kwargs: Any) -> None:
        """
        The `reinitialize` method reinitializes the Senzing objects using a specific configuration
        identifier. A list of available configuration identifiers can be retrieved using
        `szconfigmanager.get_configs`.

        Args:
            config_id (int): The configuration ID used for the initialization

        Raises:
            TypeError: Incorrect datatype of input parameter.
            szexception.SzError: config_id does not exist.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szabstractfactory/reinitialize.py
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
