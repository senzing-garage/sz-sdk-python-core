#! /usr/bin/env python3

"""
TODO: g2configmgr_abstract.py
"""

from abc import ABC, abstractmethod
from typing import Any

# Metadata

__all__ = ["G2ConfigMgrAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

# -----------------------------------------------------------------------------
# G2ConfigMgrAbstract
# -----------------------------------------------------------------------------


class G2ConfigMgrAbstract(ABC):
    """
    G2 config-manager module access library
    """

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    PREFIX = "g2configmgr."
    ID_MESSAGES = {
        4001: PREFIX + "G2ConfigMgr_addConfig({0}, {1}) failed. Return code: {2}",
        4002: PREFIX + "G2ConfigMgr_destroy() failed. Return code: {0}",
        4003: PREFIX + "G2ConfigMgr_getConfig({0}) failed. Return code: {1}",
        4004: PREFIX + "G2ConfigMgr_getConfigList() failed. Return code: {0}",
        4005: PREFIX + "G2ConfigMgr_getDefaultConfigID() failed. Return code: {0}",
        4006: PREFIX + "G2ConfigMgr_getLastException() failed. Return code: {0}",
        4007: PREFIX + "G2ConfigMgr_init({0}, {1}, {2}) failed. Return code: {3}",
        4008: PREFIX
        + "G2ConfigMgr_replaceDefaultConfigID({0}, {1}) failed. Return code: {2}",
        4009: PREFIX + "G2ConfigMgr_setDefaultConfigID({0}) failed. Return code: {1}",
    }

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def add_config(
        self, config_str: str, config_comments: str, *args: Any, **kwargs: Any
    ) -> int:
        """
        The `add_config` method adds a Senzing configuration JSON document to the Senzing database.

        Args:
            config_str (str): The Senzing configuration JSON document.
            config_comments (str):  free-form string of comments describing the configuration document.

        Returns:
            int: A configuration identifier.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2configmgr_add_config.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def destroy(self, *args: Any, **kwargs: Any) -> None:
        """
        The `destroy` method will destroy and perform cleanup for the Senzing G2ConfigMgr object.
        It should be called after all other calls are complete.

        **Note:** If the `G2ConfigMgr` constructor was called with parameters,
        the destructor will automatically call the destroy() method.
        In this case, a separate call to `destroy()` is not needed.

        Example:

        .. code-block:: python

            g2_configmgr = g2configmgr.G2ConfigMgr(MODULE_NAME, INI_PARAMS)

        Raises:
            None: No exceptions raised

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2configmgr_init_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def get_config(self, config_id: int, *args: Any, **kwargs: Any) -> str:
        """
        The `get_config` method retrieves a specific Senzing configuration JSON document from the Senzing database.

        Args:
            config_id (int): The configuration identifier of the desired Senzing Engine configuration JSON document to retrieve.

        Returns:
            str: A JSON document containing the Senzing configuration.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2configmgr_get_config.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2configmgr_get_config.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_config_list(self, *args: Any, **kwargs: Any) -> str:
        """
        The `get_config_list` method retrieves a list of Senzing configurations from the Senzing database.

        Returns:
            str: A JSON document containing Senzing configurations.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2configmgr_get_config_list.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/g2configmgr_get_config_list.txt
                :linenos:
                :language: json
        """

    @abstractmethod
    def get_default_config_id(self, *args: Any, **kwargs: Any) -> int:
        """
        The `get_default_config_id` method retrieves from the Senzing database the configuration identifier of the default Senzing configuration.

        Returns:
            int:  A configuration identifier which identifies the current configuration in use.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2configmgr_get_default_config_id.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def init(
        self, module_name: str, ini_params: str, verbose_logging: int = 0, **kwargs: Any
    ) -> None:
        """
        The `init` method initializes the Senzing G2ConfigMgr object.
        It must be called prior to any other calls.

        **Note:** If the G2ConfigMgr constructor is called with parameters,
        the constructor will automatically call the `init()` method.
        In this case, a separate call to `init()` is not needed.

        Example:

        .. code-block:: python

            g2_configmgr = g2configmgr.G2ConfigMgr(MODULE_NAME, INI_PARAMS)

        Args:
            module_name (str): A name for the auditing node, to help identify it within system logs.
            ini_params (str): A JSON string containing configuration parameters.
            verbose_logging (int): `Optional:` A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging. Default: 0

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2configmgr_init_and_destroy.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def replace_default_config_id(
        self, old_config_id: int, new_config_id: int, *args: Any, **kwargs: Any
    ) -> None:
        """
        The `replace_default_config_id` method replaces the old configuration identifier with a new configuration identifier in the Senzing database.
        It is like a "compare-and-swap" instruction to serialize concurrent editing of configuration.
        If `old_config_id` is no longer the "old configuration identifier", the operation will fail.
        To simply set the default configuration ID, use `set_default_config_id`.

        Args:
            old_config_id (int): The configuration identifier to replace.
            new_config_id (int): The configuration identifier to use as the default.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2configmgr_replace_default_config_id.py
                :linenos:
                :language: python
        """

    @abstractmethod
    def set_default_config_id(self, config_id: int, *args: Any, **kwargs: Any) -> None:
        """
        The `set_default_config_id` method replaces the sets a new configuration identifier in the Senzing database.
        To serialize modifying of the configuration identifier, see `replace_default_config_id`.

        Args:
            config_id (int): The configuration identifier of the Senzing Engine configuration to use as the default.

        .. collapse:: Example:

            .. literalinclude:: ../../examples/g2configmgr_set_default_config_id.py
                :linenos:
                :language: python
        """

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
