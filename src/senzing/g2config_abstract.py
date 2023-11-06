#! /usr/bin/env python3

"""
TODO: g2config_abstract.py
"""

from abc import ABC, abstractmethod
from typing import Any

# Metadata

__all__ = ["G2ConfigAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

# -----------------------------------------------------------------------------
# G2ConfigAbstract
# -----------------------------------------------------------------------------


class G2ConfigAbstract(ABC):
    """
    G2 config module access library
    """

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    PREFIX = "g2config."
    ID_MESSAGES = {
        4001: PREFIX + "G2Config_addDataSource({0}, {1}) failed. Return code: {2}",
        4002: PREFIX + "G2Config_close({0}) failed. Return code: {1}",
        4003: PREFIX + "G2Config_create() failed. Return code: {0}",
        4004: PREFIX + "G2Config_deleteDataSource({0}, {1}) failed. Return code: {2}",
        4005: PREFIX + "G2Config_getLastException() failed. Return code: {0}",
        4006: PREFIX + "G2Config_destroy() failed. Return code: {0}",
        4007: PREFIX + "G2Config_init({0}, {1}, {2}) failed. Return code: {3}",
        4008: PREFIX + "G2Config_listDataSources() failed. Return code: {0}",
        4009: PREFIX + "G2Config_load({0}) failed. Return code: {1}",
        4010: PREFIX + "G2Config_save({0}) failed. Return code: {1}",
    }

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def add_data_source(
        self, config_handle: int, input_json: str, *args: Any, **kwargs: Any
    ) -> str:
        """
        The `add_data_source` method adds a data source to an existing in-memory configuration.

        Args:
            config_handle (int): An identifier of an in-memory configuration. Usually created by the `create` or `load` methods.
            input_json (str):  A JSON document in the format `{"DSRC_CODE": "NAME_OF_DATASOURCE"}`.

        Returns:
            str: A string containing a JSON document listing the newly created data source.

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2config/add_data_source.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2config/add_data_source.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def close(self, config_handle: int, *args: Any, **kwargs: Any) -> None:
        """
        The `close` method cleans up the Senzing G2Config object pointed to by the `config_handle`.

        Args:
            config_handle (int): An identifier of an in-memory configuration. Usually created by the `create` or `load` methods.

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2config/create_and_close.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def create(self, *args: Any, **kwargs: Any) -> int:
        """
        The `create` method creates an in-memory Senzing configuration
        from the `g2config.json` template configuration file located
        in the PIPELINE.RESOURCEPATH path.
        A handle is returned to identify the in-memory configuration.
        The handle is used by the `add_data_source`, `list_data_sources`,
        `delete_data_source`, and `save` methods.
        The handle is terminated by the `close` method.

        Returns:
            int: A pointer to an in-memory Senzing configuration.

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2config/create_and_close.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def delete_data_source(
        self, config_handle: int, input_json: str, *args: Any, **kwargs: Any
    ) -> None:
        """
        The `delete_data_source` method removes a data source from an existing in-memory configuration.

        Args:
            config_handle (int): An identifier of an in-memory configuration. Usually created by the `create` or `load` methods
            input_json (str): A JSON document in the format `{"DSRC_CODE": "NAME_OF_DATASOURCE"}`.

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2config/delete_data_source.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2config/delete_data_source.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def destroy(self, *args: Any, **kwargs: Any) -> None:
        """
        The `destroy` method will destroy and perform cleanup for the Senzing G2Config object.
        It should be called after all other calls are complete.

        **Note:** If the `G2Config` constructor was called with parameters,
        the destructor will automatically call the destroy() method.
        In this case, a separate call to `destroy()` is not needed.

        Example:

        .. code-block:: python

            g2_config = g2config.G2Config(MODULE_NAME, INI_PARAMS)

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2config/init_and_destroy.py
                :linenos:
                :language: python

        """

    @abstractmethod
    def init(
        self, module_name: str, ini_params: str, verbose_logging: int = 0, **kwargs: Any
    ) -> None:
        """
        The `init` method initializes the Senzing G2Config object.
        It must be called prior to any other calls.

        **Note:** If the G2Config constructor is called with parameters,
        the constructor will automatically call the `init()` method.
        In this case, a separate call to `init()` is not needed.

        Example:

        .. code-block:: python

            g2_config = g2config.G2Config(MODULE_NAME, INI_PARAMS)

        Args:
            module_name (str): A name for the auditing node, to help identify it within system logs.
            ini_params (str): A JSON string containing configuration parameters.
            verbose_logging (int): `Optional:` A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging. Default: 0

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2config/init_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def list_data_sources(self, config_handle: int, *args: Any, **kwargs: Any) -> str:
        """
        The `list_data_sources` method returns a JSON document of data sources.

        Args:
            config_handle (int): An identifier of an in-memory configuration. Usually created by the `create` or `load` methods

        Returns:
            str: A string containing a JSON document listing all of the data sources.

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2config/list_data_sources.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2config/list_data_sources.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def load(self, json_config: str, *args: Any, **kwargs: Any) -> int:
        """
        The `load` method initializes an in-memory Senzing G2Config object from a JSON string.
        A configuration handle is returned.

        Args:
            json_config (str): A JSON document containing the Senzing configuration.

        Returns:
            int: An identifier (config_handle) of an in-memory configuration.

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2config/load.py
                :linenos:
                :language: python

            **Create, save, load, and close**

            .. literalinclude:: ../../examples/g2config/create_save_load_close.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def save(self, config_handle: int, *args: Any, **kwargs: Any) -> str:
        """
        The `save` method creates a JSON string representation of the Senzing G2Config object.

        Args:
            config_handle (int): An identifier of an in-memory configuration. Usually created by the `create` or `load` methods

        Returns:
            str: A string containing a JSON Document representation of the Senzing G2Config object.

        Raises:
            None: TODO:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2config/save.py
                :linenos:
                :language: python

            **Create, save, load, and close**

            .. literalinclude:: ../../examples/g2config/create_save_load_close.py
                :linenos:
                :language: python
        """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
