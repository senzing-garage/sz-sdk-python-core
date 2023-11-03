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
        The
        :py:meth:`senzing.g2config.add_data_source`
        method adds a data source to an existing in-memory configuration.
        The `config_handle` is created by the
        :py:meth:`senzing.g2config.create<create>`
        method.

        Args:
            config_handle (int): An identifier of an in-memory configuration.
            input_json (str):  A JSON document in the format `{"DSRC_CODE": "NAME_OF_DATASOURCE"}`.

        Returns:
            str: A string containing a JSON document listing the newly created data source.
        """

    @abstractmethod
    def close(self, config_handle: int, *args: Any, **kwargs: Any) -> None:
        """
        The
        :py:meth:`senzing.g2config.close`
        method cleans up the Senzing G2Config object pointed to by the `config_handle`.
        The handle was created by the
        :py:meth:`senzing.g2config.create<create>`
        method.

        Args:
            config_handle (int): An identifier of an in-memory configuration.
        """

    @abstractmethod
    def create(self, *args: Any, **kwargs: Any) -> int:
        """
        The
        :py:meth:`senzing.g2config.create`
        method creates an in-memory Senzing configuration from the `g2config.json`
        template configuration file located in the PIPELINE.RESOURCEPATH path.
        A handle is returned to identify the in-memory configuration.
        The handle is used by the
        :py:meth:`senzing.g2config.add_data_source<add_data_source>`,
        :py:meth:`senzing.g2config.list_data_sources<list_data_sources>`,
        :py:meth:`senzing.g2config.delete_data_source<delete_data_source>`,
        and
        :py:meth:`senzing.g2config.save<save>`
        methods.
        The handle is terminated by the
        :py:meth:`senzing.g2config.close<close>`
        method.

        Returns:
            int: _description_
        """

    @abstractmethod
    def delete_data_source(
        self, config_handle: int, input_json: str, *args: Any, **kwargs: Any
    ) -> None:
        """TODO: document"""

    @abstractmethod
    def destroy(self, *args: Any, **kwargs: Any) -> None:
        """TODO: document"""

    @abstractmethod
    def init(
        self,
        module_name: str,
        ini_params: str,
        verbose_logging: int,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """TODO: document"""

    @abstractmethod
    def list_data_sources(self, config_handle: int, *args: Any, **kwargs: Any) -> str:
        """TODO: document"""

    @abstractmethod
    def load(self, json_config: str, *args: Any, **kwargs: Any) -> int:
        """TODO: document"""

    @abstractmethod
    def save(self, config_handle: int, *args: Any, **kwargs: Any) -> str:
        """TODO: document"""

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
