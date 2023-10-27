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
        """TODO: document"""

    @abstractmethod
    def destroy(self, *args: Any, **kwargs: Any) -> None:
        """TODO: document"""

    @abstractmethod
    def get_config(self, config_id: int, *args: Any, **kwargs: Any) -> str:
        """TODO: document"""

    @abstractmethod
    def get_config_list(self, *args: Any, **kwargs: Any) -> str:
        """TODO: document"""

    @abstractmethod
    def get_default_config_id(self, *args: Any, **kwargs: Any) -> int:
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
    def replace_default_config_id(
        self, old_config_id: int, new_config_id: int, *args: Any, **kwargs: Any
    ) -> None:
        """TODO: document"""

    @abstractmethod
    def set_default_config_id(self, config_id: int, *args: Any, **kwargs: Any) -> None:
        """TODO: document"""

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
