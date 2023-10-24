#! /usr/bin/env python3

"""
TODO: g2hasher_grpc.py
"""

# Import from standard library. https://docs.python.org/3/library/

from typing import Any

# from .g2exception import translate_exception
from .g2hasher_abstract import G2HasherAbstract

# from ctypes import *
# import functools
# import json
# import os
# import threading
# import warnings

# Import from https://pypi.org/

# Import from Senzing.


# Metadata

__all__ = ["G2HasherGrpc"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

SENZING_PRODUCT_ID = "5055"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md

# -----------------------------------------------------------------------------
# G2HasherGrpc class
# -----------------------------------------------------------------------------


class G2HasherGrpc(G2HasherAbstract):
    """
    G2 product module access library
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        module_name: str,
        ini_params: str,
        verbose_logging: int,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """

        self.ini_params = ini_params
        self.module_name = module_name
        self.noop = ""
        self.verbose_logging = verbose_logging

        self.init(self.module_name, self.ini_params, self.verbose_logging)

    def __del__(self) -> None:
        """Destructor"""
        self.destroy()

    # -------------------------------------------------------------------------
    # Development methods - to be removed after initial development
    # -------------------------------------------------------------------------

    def fake_g2hasher(self, *args: Any, **kwargs: Any) -> None:
        """TODO: Remove once SDK methods have been implemented."""
        if len(args) + len(kwargs) > 2000:
            print(self.noop)

    # -------------------------------------------------------------------------
    # G2Hasher methods
    # -------------------------------------------------------------------------

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        self.fake_g2hasher()

    def export_token_library(self, *args: Any, **kwargs: Any) -> str:
        self.fake_g2hasher()
        return "response"

    def init(
        self,
        module_name: str,
        ini_params: str,
        verbose_logging: int,
        *args: Any,
        **kwargs: Any
    ) -> None:
        self.fake_g2hasher(module_name, ini_params, verbose_logging)

    def init_with_config_id(
        self,
        module_name: str,
        ini_params: str,
        init_config_id: int,
        verbose_logging: int,
        *args: Any,
        **kwargs: Any
    ) -> None:
        self.fake_g2hasher(module_name, ini_params, init_config_id, verbose_logging)

    def process(self, record: str, *args: Any, **kwargs: Any) -> str:
        self.fake_g2hasher(record)
        return "response"

    def reinit(self, init_config_id: int, *args: Any, **kwargs: Any) -> None:
        self.fake_g2hasher(init_config_id)
