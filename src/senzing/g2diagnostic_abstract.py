#! /usr/bin/env python3

"""
TODO: g2diagnostic_abstract.py
"""

# Import from standard library. https://docs.python.org/3/library/

from abc import ABC, abstractmethod


class G2DiagnosticAbstract(ABC):
    """
    G2 diagnostic module access library
    """

    @abstractmethod
    def check_db_perf(self, seconds_to_run: int, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def destroy(self, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def get_available_memory(self, *args, **kwargs) -> int:
        """TODO: document"""

    @abstractmethod
    def get_db_info(self, *args, **kwargs) -> str:
        """TODO: document"""

    @abstractmethod
    def get_logical_cores(self, *args, **kwargs) -> int:
        """TODO: document"""

    @abstractmethod
    def get_physical_cores(self, *args, **kwargs) -> int:
        """TODO: document"""

    @abstractmethod
    def get_total_system_memory(self, *args, **kwargs) -> int:
        """TODO: document"""

    @abstractmethod
    def init(self, module_name: str, ini_params: str, verbose_logging: int, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def init_with_config_id(self, module_name: str, ini_params: str, init_config_id: int, verbose_logging: int, *args, **kwargs) -> None:
        """TODO: document"""

    @abstractmethod
    def reinit(self, init_config_id: int, *args, **kwargs) -> None:
        """TODO: document"""
