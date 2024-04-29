#! /usr/bin/env python3

"""
szconfig_abstract.py is the abstract class for all implementations of szconfig.
"""

# TODO: Determine specific SzErrors, Errors for "Raises:" documentation.

from abc import ABC, abstractmethod
from typing import Any, Dict, Union

# Metadata

__all__ = ["SzConfigAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-08"

# -----------------------------------------------------------------------------
# SzConfigAbstract
# -----------------------------------------------------------------------------


class SzConfigAbstract(ABC):
    """
    SzConfigAbstract is the definition of the Senzing Python API that is
    implemented by packages such as szconfig.py.
    """

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    PREFIX = "szconfig."
    ID_MESSAGES = {
        4001: PREFIX + "add_data_source({0}) failed. Return code: {1}",
        4002: PREFIX + "close_config() failed. Return code: {0}",
        4003: PREFIX + "create_config() failed. Return code: {0}",
        4004: PREFIX + "delete_data_source({0}) failed. Return code: {1}",
        4005: PREFIX + "destroy() failed. Return code: {0}",
        4006: PREFIX + "export_config() failed. Return code: {0}",
        4007: PREFIX + "get_data_sources() failed. Return code: {0}",
        4008: PREFIX + "initialize({0}, {1}, {2}) failed. Return code: {3}",
        4009: PREFIX + "import_config({0}) failed. Return code: {1}",
        4010: PREFIX
        + "SzConfig({0}, {1}) failed. instance_name and settings must both be set or both be empty",
    }

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def add_data_source(
        self,
        config_handle: int,
        # data_source_code: Union[str, Dict[Any, Any]],
        data_source_code: str,
        **kwargs: Any
    ) -> str:
        """
        The `add_data_source` method adds a data source to an existing in-memory configuration.

        Args:
            config_handle (int): An identifier of an in-memory configuration. Usually created by the `create` or `load` methods.
            data_source_code (str): Name of data source code to add.

        Returns:
            str: A string containing a JSON document listing the newly created data source.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfig/add_data_source.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szconfig/add_data_source.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def close_config(self, config_handle: int, **kwargs: Any) -> None:
        """
        The `close_config` method cleans up the Senzing SzConfig object pointed to by the `config_handle`.

        Args:
            config_handle (int): An identifier of an in-memory configuration. Usually created by the `create_config` or `import_config` methods.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfig/create_and_close.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def create_config(self, **kwargs: Any) -> int:
        """
        The `create_config` method creates an in-memory Senzing configuration
        from the `g2config.json` template configuration file located
        in the PIPELINE.RESOURCEPATH path.
        A handle is returned to identify the in-memory configuration.
        The handle is used by the `add_data_source`, `list_data_sources`,
        `delete_data_source`, and `export_config` methods.
        The handle is terminated by the `close_config` method.

        Returns:
            int: A pointer to an in-memory Senzing configuration.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfig/create_and_close.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def delete_data_source(
        self, config_handle: int, data_source_code: str, **kwargs: Any
    ) -> None:
        """
        The `delete_data_source` method removes a data source from an existing in-memory configuration.

        Args:
            config_handle (int): An identifier of an in-memory configuration. Usually created by the `create` or `load` methods
            data_source_code (str): Name of data source code to delete.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfig/delete_data_source.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def destroy(self, **kwargs: Any) -> None:
        """
        The `destroy` method will destroy and perform cleanup for the Senzing SzConfig object.
        It should be called after all other calls are complete.

        **Note:** If the `SzConfig` constructor was called with parameters,
        the destructor will automatically call the destroy() method.
        In this case, a separate call to `destroy()` is not needed.

        Raises:
            szerror.SzError:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfig/szconfig_initialize_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def export_config(self, config_handle: int, **kwargs: Any) -> str:
        """
        The `export_config` method creates a JSON string representation of the Senzing SzConfig object.

        Args:
            config_handle (int): An identifier of an in-memory configuration. Usually created by the `create` or `load` methods

        Returns:
            str: A string containing a JSON Document representation of the Senzing SzConfig object.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfig/export_config.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szconfig/export_config.txt
                :linenos:
                :language: json

            **Create, export, import, and close example**

            .. literalinclude:: ../../examples/szconfig/create_export_import_close.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def get_data_sources(self, config_handle: int, **kwargs: Any) -> str:
        """
        The `get_data_sources` method returns a JSON document of data sources
        contained in an in-memory configuration.

        Args:
            config_handle (int): An identifier of an in-memory configuration. Usually created by the `create` or `load` methods

        Returns:
            str: A string containing a JSON document listing all of the data sources.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfig/get_data_sources.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szconfig/get_data_sources.txt
                :linenos:
                :language: json
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
        The `initialize` method initializes the Senzing SzConfig object.
        It must be called prior to any other calls.

        **Note:** If the SzConfig constructor is called with parameters,
        the constructor will automatically call the `initialize()` method.
        In this case, a separate call to `initialize()` is not needed.

        Args:
            instance_name (str): A short name given to this instance of the SzConfig object, to help identify it within system logs.
            settings (Union[str, Dict[Any, Any]]): A JSON string containing configuration parameters.
            verbose_logging (int): `Optional:` A flag to enable deeper logging of the Senzing processing. 0 for no Senzing logging; 1 for logging. Default: 0

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfig/szconfig_initialize_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def import_config(
        self, config_definition: Union[str, Dict[Any, Any]], **kwargs: Any
    ) -> int:
        """
        The `import_config` method initializes an in-memory Senzing SzConfig object from a JSON string.
        A handle is returned to identify the in-memory configuration.
        The handle is used by the `add_data_source`, `get_data_sources`,
        `delete_data_source`, and `save` methods.
        The handle is terminated by the `close` method.

        Args:
            config_definition (Union[str, Dict[Any, Any]]): A JSON document containing the Senzing configuration.

        Returns:
            int: An identifier (config_handle) of an in-memory configuration.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfig/import_config.py
                :linenos:
                :language: python

            **Create, save, load, and close**

            .. literalinclude:: ../../examples/szconfig/create_export_import_close.py
                :linenos:
                :language: python
        """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
