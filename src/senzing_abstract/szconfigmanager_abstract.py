#! /usr/bin/env python3

"""
szconfigmanager_abstract.py is the abstract class for all implementations of szconfigmanager.
"""

# TODO: Determine specific SzErrors, Errors for "Raises:" documentation.

from abc import ABC, abstractmethod
from typing import Any

from .szhelpers import construct_help

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
    # Messages
    # -------------------------------------------------------------------------

    PREFIX = "szconfigmanager."
    ID_MESSAGES = {
        4001: PREFIX + "add_config({0}, {1}) failed. Return code: {2}",
        4002: PREFIX + "destroy() failed. Return code: {0}",
        4003: PREFIX + "get_config({0}) failed. Return code: {1}",
        4004: PREFIX + "get_configs() failed. Return code: {0}",
        4005: PREFIX + "get_default_config_id() failed. Return code: {0}",
        4006: PREFIX + "initialize({0}, {1}, {2}) failed. Return code: {3}",
        4007: PREFIX + "replace_default_config_id({0}, {1}) failed. Return code: {2}",
        4008: PREFIX + "set_default_config_id({0}) failed. Return code: {1}",
        4009: PREFIX
        + "SzConfigManager({0}, {1}) failed. instance_name and settings must both be set or both be empty",
    }

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

    def help(self, method_name: str = "") -> str:
        """
        Return the help for a particular message.

        Args:
            method_name (str): The name of the method. (e.g. "init"). If empty, a list of methods and descriptions is returned.

        Returns:
            str: The Help information about the requested method
        """
        return construct_help(self, method_name=method_name)
