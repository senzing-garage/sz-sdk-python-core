#! /usr/bin/env python3

"""
szconfigmgr_abstract.py is the abstract class for all implementations of szconfigmgr.
"""

# TODO: Determine specific G2Exceptions, Errors for "Raises:" documentation.

from abc import ABC, abstractmethod
from typing import Any, Dict, Union

# Metadata

__all__ = ["SzConfigManagerAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-08"

# -----------------------------------------------------------------------------
# G2ConfigMgrAbstract
# -----------------------------------------------------------------------------


class SzConfigManagerAbstract(ABC):
    """
    SzConfigMgrAbstract is the definition of the Senzing Python API that is
    implemented by packages such as szconfigmgr.py.
    """

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    PREFIX = "szconfigmanager."
    # TODO: remove + concats for f-strings
    ID_MESSAGES = {
        4001: PREFIX + "add_config({0}, {1}) failed. Return code: {2}",
        4002: PREFIX + "destroy() failed. Return code: {0}",
        4003: PREFIX + "get_config({0}) failed. Return code: {1}",
        4004: PREFIX + "get_config_list() failed. Return code: {0}",
        4005: PREFIX + "get_default_config_id() failed. Return code: {0}",
        4006: PREFIX + "initialize({0}, {1}, {2}) failed. Return code: {3}",
        4007: PREFIX + "replace_default_config_id({0}, {1}) failed. Return code: {2}",
        4008: PREFIX + "set_default_config_id({0}) failed. Return code: {1}",
        4009: PREFIX
        + "SzConfigManager({0}, {1}) must have both module_name and ini_params nor neither.",
    }

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def add_config(
        self,
        config_definition: Union[str, Dict[Any, Any]],
        config_comment: str,
        **kwargs: Any
    ) -> int:
        """
        The `add_config` method adds a Senzing configuration JSON document to the Senzing database.

        Args:
            config_definition (Union[str, Dict[Any, Any]]): The Senzing configuration JSON document.
            config_comment (str):  free-form string of comments describing the configuration document.

        Returns:
            int: A configuration identifier.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmgr/add_config.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def destroy(self, **kwargs: Any) -> None:
        """
        The `destroy` method will destroy and perform cleanup for the Senzing SzConfigMgr object.
        It should be called after all other calls are complete.

        **Note:** If the `SzConfigManager` constructor was called with parameters,
        the destructor will automatically call the destroy() method.
        In this case, a separate call to `destroy()` is not needed.

        Example:

        .. code-block:: python

            sz_configmgr = szconfigmgr.SzConfigMgr(module_name, ini_params)

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmgr/szconfigmgr_init_and_destroy.py
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

            .. literalinclude:: ../../examples/szconfigmgr/get_config.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szconfigmgr/get_config.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_config_list(self, **kwargs: Any) -> str:
        """
        The `get_config_list` method retrieves a list of Senzing configurations from the Senzing database.

        Returns:
            str: A JSON document containing Senzing configurations.

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmgr/get_config_list.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/szconfigmgr/get_config_list.txt
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

            .. literalinclude:: ../../examples/szconfigmgr/get_default_config_id.py
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
        The `initialize` method initializes the Senzing SzConfigMgr object.
        It must be called prior to any other calls.

        **Note:** If the SzConfigMgr constructor is called with parameters,
        the constructor will automatically call the `initialize()` method.
        In this case, a separate call to `initialize()` is not needed.

        Example:

        .. code-block:: python

            sz_configmgr = szconfigmgr.SzConfigMgr(module_name, ini_params)

        Args:
            instance_name (str): A short name given to this instance of the SzProduct object, to help identify it within system logs.
            settings (Union[str, Dict[Any, Any]]): A JSON string containing configuration parameters.
            verbose_logging (int): `Optional:` A flag to enable deeper logging of the Senzing processing. 0 for no Senzing logging; 1 for logging. Default: 0

        Raises:
            TypeError: Incorrect datatype of input parameter.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/szconfigmgr/szconfigmgr_init_and_destroy.py
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

            .. literalinclude:: ../../examples/szconfigmgr/replace_default_config_id.py
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

            .. literalinclude:: ../../examples/szconfigmgr/set_default_config_id.py
                :linenos:
                :language: python
        """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
