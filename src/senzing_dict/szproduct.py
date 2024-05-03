"""
TODO: Create documentation
"""

# pylint: disable=R0903

import json
from types import TracebackType
from typing import Any, Callable, Dict, Type, Union

from senzing_abstract import SzProductAbstract

# Metadata

__all__ = ["SzProduct"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2024-05-03"
__updated__ = "2024-05-03"


def default_dict_function(input_string: str) -> Dict[str, Any]:
    result: Dict[str, Any] = json.loads(input_string)
    return result


# -----------------------------------------------------------------------------
# SzProduct class
# -----------------------------------------------------------------------------


class SzProduct:
    """
    TODO: Create documentation
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        sz_product: SzProductAbstract,
        dict_function: Callable[[str], Dict[str, Any]] = default_dict_function,
        **kwargs: Any,
    ) -> None:
        """
        TODO: Create documentation
        """

        # Verify parameters.

        self.sz_product = sz_product
        self.dict_function = dict_function

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
    # SzProduct methods
    # -------------------------------------------------------------------------

    def get_license(self, **kwargs: Any) -> Dict[str, Any]:
        return self.dict_function(self.sz_product.get_license())

    def get_version(self, **kwargs: Any) -> Dict[str, Any]:
        return self.dict_function(self.sz_product.get_version())
