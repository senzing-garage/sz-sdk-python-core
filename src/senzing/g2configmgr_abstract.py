#! /usr/bin/env python3

"""
TODO: g2configmgr_abstract.py
"""

# Import from standard library. https://docs.python.org/3/library/

from abc import ABC, abstractmethod
from typing import Any

# Metadata

__all__ = ["G2ConfigMgrAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"


class G2ConfigMgrAbstract(ABC):
    """
    G2 config-manager module access library
    """

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
