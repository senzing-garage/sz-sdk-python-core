#! /usr/bin/env python3

"""
TODO: g2product_grpc.py
"""

# Import from standard library. https://docs.python.org/3/library/

# from ctypes import *
# import functools
# import json
# import os
# import threading
# import warnings

# Import from https://pypi.org/

# Import from Senzing.

from typing import Any, Dict, Union

from .g2helpers import as_str

# from .g2exception import translate_exception
from .g2product_abstract import G2ProductAbstract

# Metadata

__all__ = ["G2ProductGrpc"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-27"

SENZING_PRODUCT_ID = "5056"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md

# -----------------------------------------------------------------------------
# G2ProductGrpc class
# -----------------------------------------------------------------------------


class G2ProductGrpc(G2ProductAbstract):
    """
    G2 product module access library
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        module_name: str = "",
        ini_params: Union[str, Dict[Any, Any]] = "",
        init_config_id: int = 0,
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """
        # pylint: disable=W0613

        self.ini_params = as_str(ini_params)
        self.init_config_id = init_config_id
        self.module_name = module_name
        self.noop = ""
        self.verbose_logging = verbose_logging

    def __del__(self) -> None:
        """Destructor"""
        self.destroy()

    # -------------------------------------------------------------------------
    # Development methods - to be removed after initial development
    # -------------------------------------------------------------------------

    def fake_g2config(self, *args: Any, **kwargs: Any) -> None:
        """TODO: Remove once SDK methods have been implemented."""
        if len(args) + len(kwargs) > 2000:
            print(self.noop)

    # -------------------------------------------------------------------------
    # G2Product methods
    # -------------------------------------------------------------------------

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        self.fake_g2config()

    def init(
        self,
        module_name: str,
        ini_params: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        self.fake_g2config(module_name, ini_params, verbose_logging)

    def license(self, *args: Any, **kwargs: Any) -> str:
        self.fake_g2config()
        return "string"

    def version(self, *args: Any, **kwargs: Any) -> str:
        self.fake_g2config()
        return "string"
