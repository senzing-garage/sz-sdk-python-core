"""
TODO: Create documentation
"""

# pylint: disable=R0903


import json
from types import TracebackType
from typing import Any, Callable, Dict, Type, Union

from senzing._helpers import as_str
from senzing_abstract import SzConfigAbstract

# from senzing import as_str


# Metadata

__all__ = ["SzConfig"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2024-05-03"
__updated__ = "2024-05-03"


def default_dict_function(input_string: str) -> Dict[str, Any]:
    """TODO: Create documentation"""
    result: Dict[str, Any] = json.loads(input_string)
    return result


# -----------------------------------------------------------------------------
# SzConfig class
# -----------------------------------------------------------------------------


class SzConfig:
    """
    TODO: Create documentation
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        sz_config: SzConfigAbstract,
        dict_function: Callable[[str], Dict[str, Any]] = default_dict_function,
        **kwargs: Any,
    ) -> None:
        """TODO: Create documentation"""

        self.sz_config = sz_config
        self.dict_function = dict_function
        _ = kwargs

    def __enter__(
        self,
    ) -> (
        Any
    ):  # TODO: Replace "Any" with "Self" once python 3.11 is lowest supported python version.
        """Context Manager method."""
        return self

    def __exit__(
        self,
        exc_type: Union[Type[BaseException], None],
        exc_val: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ) -> None:
        """Context Manager method."""

    # -------------------------------------------------------------------------
    # SzConfig methods
    # -------------------------------------------------------------------------

    def add_data_source(
        self,
        config_handle: int,
        data_source_code: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_config.add_data_source(config_handle, data_source_code, **kwargs)
        )

    def close_config(self, config_handle: int, **kwargs: Any) -> None:
        """TODO: Create documentation"""
        return self.sz_config.close_config(config_handle, **kwargs)

    def create_config(self, **kwargs: Any) -> int:
        """TODO: Create documentation"""
        return self.sz_config.create_config(**kwargs)

    def delete_data_source(
        self,
        config_handle: int,
        data_source_code: str,
        **kwargs: Any,
    ) -> None:
        """TODO: Create documentation"""
        return self.sz_config.delete_data_source(
            config_handle, data_source_code, **kwargs
        )

    def export_config(self, config_handle: int, **kwargs: Any) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(self.sz_config.export_config(config_handle, **kwargs))

    def get_data_sources(self, config_handle: int, **kwargs: Any) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_config.get_data_sources(config_handle, **kwargs)
        )

    # TODO
    # def initialize(
    #     self,
    #     instance_name: str,
    #     settings: Union[str, Dict[Any, Any]],
    #     verbose_logging: int = 0,
    #     **kwargs: Any,
    # ) -> None:
    #     """TODO: Create documentation"""
    #     return self.sz_config.initialize(
    #         instance_name, settings, verbose_logging, **kwargs
    #     )

    def import_config(
        self, config_definition: Union[str, Dict[Any, Any]], **kwargs: Any
    ) -> int:
        """TODO: Create documentation"""
        return self.sz_config.import_config(as_str(config_definition), **kwargs)
