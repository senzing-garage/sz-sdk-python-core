#! /usr/bin/env python3

"""
TODO: g2product_abstract.py
"""

from abc import ABC, abstractmethod
from typing import Any

# Metadata

__all__ = ["G2ProductAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

# -----------------------------------------------------------------------------
# G2ProductAbstract
# -----------------------------------------------------------------------------


class G2ProductAbstract(ABC):
    """
    G2 product module access library
    """

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    PREFIX = "g2product."
    ID_MESSAGES = {
        4001: PREFIX + "G2Product_destroy() failed. Return code: {0}",
        4002: PREFIX + "G2Product_getLastException() failed. Return code: {0}",
        4003: PREFIX + "G2Product_init({0}, {1}, {2}) failed. Return code: {3}",
    }

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

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
    def license(self, *args: Any, **kwargs: Any) -> str:
        """TODO: document"""

    @abstractmethod
    def version(self, *args: Any, **kwargs: Any) -> str:
        """TODO: document"""

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
