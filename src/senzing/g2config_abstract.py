#! /usr/bin/env python3

"""
TODO: g2config_abstract.py
"""

# Import from standard library. https://docs.python.org/3/library/

from abc import ABC, abstractmethod

# Metadata

__all__ = ["G2ConfigAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"


class G2ConfigAbstract(ABC):
    """
    G2 config module access library
    """

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def add_data_source(
        self, config_handle: int, input_json: str, *args, **kwargs
    ) -> str:
        """TODO: document"""

    @abstractmethod
    def close(self, config_handle: int, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def create(self, *args, **kwargs) -> int:
        """TODO: document"""

    @abstractmethod
    def delete_data_source(
        self, config_handle: int, input_json: str, *args, **kwargs
    ) -> None:
        """TODO: document"""

    @abstractmethod
    def destroy(self, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def init(
        self, module_name: str, ini_params: str, verbose_logging: int, *args, **kwargs
    ) -> None:
        """TODO: document"""

    @abstractmethod
    def list_data_sources(self, config_handle: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def load(self, json_config: str, *args, **kwargs) -> int:
        """TODO: document"""

    @abstractmethod
    def save(self, config_handle: int, *args, **kwargs) -> str:
        """TODO: document"""

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
