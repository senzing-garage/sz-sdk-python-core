"""
szconfigmanager_abstract.py is the abstract class for all implementations of szconfigmanager.
"""

# TODO: Determine specific SzErrors, Errors for "Raises:" documentation.

from abc import ABC, abstractmethod
from typing import Any, Dict, Union

# Metadata

__all__ = ["SzConfigManagerAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-08"

# -----------------------------------------------------------------------------
# SzConfigManagerAbstract
# -----------------------------------------------------------------------------


class SzConfigManagerAbstract(ABC):
    """
    SzConfigManagerAbstract is the definition of the Senzing Python API that is
    implemented by packages such as szconfigmanager.py.
    """

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def add_config(
        self, config_definition: str, config_comment: str, **kwargs: Any
    ) -> int:
        """
        The `add_config` method adds a Senzing configuration JSON document to the Senzing database.

        Args:
            config_definition (str): The Senzing configuration JSON document.
            config_comment (str):  free-form string of comments describing the configuration document.

        Returns:
            int: A configuration identifier.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/add_config.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def destroy(self, **kwargs: Any) -> None:
        """
        The `destroy` method will destroy and perform cleanup for the Senzing SzConfigManager object.
        It should be called after all other calls are complete.

        **Note:** If the `SzConfigManager` constructor was called with parameters,
        the destructor will automatically call the destroy() method.
        In this case, a separate call to `destroy()` is not needed.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/szconfigmanager_initialize_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def get_config(self, config_id: int, **kwargs: Any) -> str:
        """
        The `get_config` method retrieves a specific Senzing configuration JSON document from the Senzing database.

        Args:
            config_id (int): The configuration identifier of the desired Senzing Engine configuration JSON document to retrieve.

        Returns:
            str: A JSON document containing the Senzing configuration.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/get_config.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szconfigmanager/get_config.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_configs(self, **kwargs: Any) -> str:
        """
        The `get_configs` method retrieves a list of Senzing configurations from the Senzing database.

        Returns:
            str: A JSON document containing Senzing configurations.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/get_configs.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szconfigmanager/get_configs.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_default_config_id(self, **kwargs: Any) -> int:
        """
        The `get_default_config_id` method retrieves from the Senzing database the configuration identifier of the default Senzing configuration.

        Returns:
            int:  A configuration identifier which identifies the current configuration in use.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/get_default_config_id.py
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
        The `initialize` method initializes the Senzing SzConfigManager object.
        It must be called prior to any other calls.

        **Note:** If the SzConfigManager constructor is called with parameters,
        the constructor will automatically call the `initialize()` method.
        In this case, a separate call to `initialize()` is not needed.

        Args:
            instance_name (str): A short name given to this instance of the SzProduct object, to help identify it within system logs.
            settings (Union[str, Dict[Any, Any]]): A JSON string containing configuration parameters.
            verbose_logging (int): `Optional:` A flag to enable deeper logging of the Senzing processing. 0 for no Senzing logging; 1 for logging. Default: 0

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/szconfigmanager_initialize_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def replace_default_config_id(
        self, current_default_config_id: int, new_default_config_id: int, **kwargs: Any
    ) -> None:
        """
        The `replace_default_config_id` method replaces the old configuration identifier with a new configuration identifier in the Senzing database.
        It is like a "compare-and-swap" instruction to serialize concurrent editing of configuration.
        If `current_default_config_id` is no longer the "current configuration identifier", the operation will fail.
        To simply set the default configuration ID, use `set_default_config_id`.

        Args:
            current_default_config_id (int): The configuration identifier to replace.
            new_default_config_id (int): The configuration identifier to use as the default.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/replace_default_config_id.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def set_default_config_id(self, config_id: int, **kwargs: Any) -> None:
        """
        The `set_default_config_id` method replaces the sets a new configuration identifier in the Senzing database.
        To serialize modifying of the configuration identifier, see `replace_default_config_id`.

        Args:
            config_id (int): The configuration identifier of the Senzing Engine configuration to use as the default.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmanager/set_default_config_id.py
                :linenos:
                :language: python
        """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
