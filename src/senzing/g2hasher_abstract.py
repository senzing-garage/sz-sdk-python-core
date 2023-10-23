#! /usr/bin/env python3

"""
TODO: g2hasher_abstract.py
"""

# Import from standard library. https://docs.python.org/3/library/

from abc import ABC, abstractmethod

# Metadata

__all__ = ["G2HasherAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"


class G2HasherAbstract(ABC):
    """
    G2 hasher module access library
    """

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def destroy(self, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def export_token_library(self, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def init(
        self, module_name: str, ini_params: str, verbose_logging: int, *args, **kwargs
    ) -> None:
        """TODO: document"""

    @abstractmethod
    def init_with_config_id(
        self,
        module_name: str,
        ini_params: str,
        init_config_id: int,
        verbose_logging: int,
        *args,
        **kwargs
    ) -> None:
        """TODO: document"""

    @abstractmethod
    def process(self, record: str, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def reinit(self, init_config_id: int, *args, **kwargs) -> None:
        """TODO: document"""

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
