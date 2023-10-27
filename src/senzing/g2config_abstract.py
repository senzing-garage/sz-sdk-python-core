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
        """TODO: document"""

    @abstractmethod
    def close(self, config_handle: int, *args: Any, **kwargs: Any) -> None:
        """TODO: document"""

    @abstractmethod
    def create(self, *args: Any, **kwargs: Any) -> int:
        """TODO: document"""

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
