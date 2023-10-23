#! /usr/bin/env python3

"""
TODO: g2product_abstract.py
"""

# Import from standard library. https://docs.python.org/3/library/

from abc import ABC, abstractmethod

# Metadata

__all__ = ["G2ProductAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"


class G2ProductAbstract(ABC):
    """
    G2 product module access library
    """

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def destroy(self, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def init(
        self, module_name: str, ini_params: str, verbose_logging: int, *args, **kwargs
    ) -> None:
        """TODO: document"""

    @abstractmethod
    def license(self, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def version(self, *args, **kwargs) -> str:
        """TODO: document"""

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------
