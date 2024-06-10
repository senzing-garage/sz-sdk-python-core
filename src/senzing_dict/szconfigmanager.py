"""
TODO: Create documentation
"""

# pylint: disable=R0903


import json
from types import TracebackType
from typing import Any, Callable, Dict, Type, Union

from senzing_abstract import SzConfigManagerAbstract

# from senzing import as_str
from senzing.sdkhelpers import as_str

# Metadata

__all__ = ["SzConfigManager"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2024-05-03"
__updated__ = "2024-05-03"


def default_dict_function(input_string: str) -> Dict[str, Any]:
    """TODO: Create documentation"""
    result: Dict[str, Any] = json.loads(input_string)
    return result


# -----------------------------------------------------------------------------
# SzConfigManager class
# -----------------------------------------------------------------------------


class SzConfigManager:
    """
    TODO: Create documentation
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        sz_configmanager: SzConfigManagerAbstract,
        dict_function: Callable[[str], Dict[str, Any]] = default_dict_function,
        **kwargs: Any,
    ) -> None:
        """TODO: Create documentation"""

        # Verify parameters.

        self.sz_configmanager = sz_configmanager
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
    # SzConfigManager methods
    # -------------------------------------------------------------------------

    def add_config(
        self,
        config_definition: Union[str, Dict[Any, Any]],
        config_comment: str,
        **kwargs: Any,
    ) -> int:
        """TODO: Create documentation"""
        return self.sz_configmanager.add_config(
            as_str(config_definition), config_comment, **kwargs
        )

    # TODO
    # def destroy(self, **kwargs: Any) -> None:
    #     """TODO: Create documentation"""
    #     return self.sz_configmanager.destroy(**kwargs)

    def get_config(self, config_id: int, **kwargs: Any) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(self.sz_configmanager.get_config(config_id, **kwargs))

    def get_config_list(self, **kwargs: Any) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(self.sz_configmanager.get_configs(**kwargs))

    def get_default_config_id(self, **kwargs: Any) -> int:
        """TODO: Create documentation"""
        return self.sz_configmanager.get_default_config_id(**kwargs)

    # TODO
    # def initialize(
    #     self,
    #     instance_name: str,
    #     settings: Union[str, Dict[Any, Any]],
    #     verbose_logging: int = 0,
    #     **kwargs: Any,
    # ) -> None:
    #     """TODO: Create documentation"""
    #     return self.sz_configmanager.initialize(
    #         instance_name, settings, verbose_logging, **kwargs
    #     )

    def replace_default_config_id(
        self,
        current_default_config_id: int,
        new_default_config_id: int,
        **kwargs: Any,
    ) -> None:
        """TODO: Create documentation"""
        return self.sz_configmanager.replace_default_config_id(
            current_default_config_id, new_default_config_id, **kwargs
        )

    def set_default_config_id(self, config_id: int, **kwargs: Any) -> None:
        """TODO: Create documentation"""
        return self.sz_configmanager.set_default_config_id(config_id, **kwargs)
