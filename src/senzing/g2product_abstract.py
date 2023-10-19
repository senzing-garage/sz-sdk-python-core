#! /usr/bin/env python3

"""
TODO: g2product_abstract.py
"""

# Import from standard library. https://docs.python.org/3/library/

from abc import ABC, abstractmethod


class G2ProductAbstract(ABC):
    """
    G2 product module access library
    """

    @abstractmethod
    def destroy(self, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def init(self, module_name: str, ini_params: str, verbose_logging: int, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def license(self, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def version(self, *args, **kwargs) -> str:
        """TODO: document"""
