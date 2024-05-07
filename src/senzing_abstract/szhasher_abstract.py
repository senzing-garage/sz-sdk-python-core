#! /usr/bin/env python3

"""
TODO: szhasher_abstract.py
"""

from abc import ABC, abstractmethod
from typing import Any

# Metadata

__all__ = ["SzHasherAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

# -----------------------------------------------------------------------------
# SzHasherAbstract
# -----------------------------------------------------------------------------


class SzHasherAbstract(ABC):
    """
    SzHasher module access library
    """

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    PREFIX = "szhasher."
    ID_MESSAGES = {0: ""}

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def destroy(self, *args: Any, **kwargs: Any) -> None:
        """TODO: document"""

    @abstractmethod
    def export_token_library(self, *args: Any, **kwargs: Any) -> str:
        """TODO: document"""

    @abstractmethod
    def init(
        self, instance_name: str, settings: str, verbose_logging: int = 0, **kwargs: Any
    ) -> None:
        """TODO: document"""

    @abstractmethod
    def init_with_config_id(
        self,
        instance_name: str,
        settings: str,
        config_id: int,
        verbose_logging: int = 0,
        **kwargs: Any
    ) -> None:
        """TODO: document"""

    @abstractmethod
    def process(self, record: str, *args: Any, **kwargs: Any) -> str:
        """TODO: document"""

    @abstractmethod
    def reinit(self, init_config_id: int, *args: Any, **kwargs: Any) -> None:
        """TODO: document"""

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
