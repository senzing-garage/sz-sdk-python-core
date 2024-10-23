"""
TODO: Create documentation
"""

# pylint: disable=R0903,R0915

import json
from types import TracebackType
from typing import Any, Callable, Dict, Type, Union

from senzing_abstract import SzDiagnosticAbstract

# Metadata

__all__ = ["SzDiagnostic"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2024-05-03"
__updated__ = "2024-05-03"


def default_dict_function(input_string: str) -> Dict[str, Any]:
    """TODO: Create documentation"""
    result: Dict[str, Any] = json.loads(input_string)
    return result


# -----------------------------------------------------------------------------
# SzDiagnostic class
# -----------------------------------------------------------------------------


class SzDiagnostic:
    """
    TODO: Create documentation
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        sz_diagnostic: SzDiagnosticAbstract,
        dict_function: Callable[[str], Dict[str, Any]] = default_dict_function,
        **kwargs: Any,
    ) -> None:
        """TODO: Create documentation"""

        # Verify parameters.

        self.sz_diagnostic = sz_diagnostic
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
    # SzDiagnostic methods
    # -------------------------------------------------------------------------

    def check_datastore_performance(
        self, seconds_to_run: int, **kwargs: Any
    ) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(
            self.sz_diagnostic.check_datastore_performance(seconds_to_run, **kwargs)
        )

    # TODO
    # def destroy(self, **kwargs: Any) -> None:
    #     """TODO: Create documentation"""
    #     return self.sz_diagnostic.destroy(**kwargs)

    def get_datastore_info(self, **kwargs: Any) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(self.sz_diagnostic.get_datastore_info(**kwargs))

    def get_feature(self, feature_id: int, **kwargs: Any) -> Dict[str, Any]:
        """TODO: Create documentation"""
        return self.dict_function(self.sz_diagnostic.get_feature(feature_id, **kwargs))

    # TODO
    # def initialize(
    #     self,
    #     instance_name: str,
    #     settings: Union[str, Dict[Any, Any]],
    #     config_id: int = 0,
    #     verbose_logging: int = 0,
    #     **kwargs: Any,
    # ) -> None:
    #     """TODO: Create documentation"""
    #     return self.sz_diagnostic.initialize(
    #         instance_name, settings, config_id, verbose_logging, **kwargs
    #     )

    def purge_repository(self, **kwargs: Any) -> None:
        """TODO: Create documentation"""
        return self.sz_diagnostic.purge_repository(**kwargs)

    # def reinitialize(self, config_id: int, **kwargs: Any) -> None:
    #     """TODO: Create documentation"""
    #     return self.sz_diagnostic.reinitialize(
    #         config_id, **kwargs
    #     )
