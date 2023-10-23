#! /usr/bin/env python3

"""
TODO: g2config_grpc.py
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

# from .g2exception import translate_exception
from .g2config_abstract import G2ConfigAbstract

# from senzing import G2ConfigAbstract
# import g2config_abstract


# Metadata

__all__ = ["G2ConfigGrpc"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

SENZING_PRODUCT_ID = "5050"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md

# -----------------------------------------------------------------------------
# G2ConfigGrpc class
# -----------------------------------------------------------------------------


class G2ConfigGrpc(G2ConfigAbstract):
    """
    G2 config module access library
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self, module_name: str, ini_params: str, verbose_logging: int, *args, **kwargs
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

    def fake_g2config(self, *args, **kwargs):
        """TODO: Remove once SDK methods have been implemented."""
        if len(args) + len(kwargs) > 2000:
            print(self.noop)

    # -------------------------------------------------------------------------
    # G2Config methods
    # -------------------------------------------------------------------------

    def add_data_source(
        self, config_handle: int, input_json: str, *args, **kwargs
    ) -> str:
        self.fake_g2config(config_handle, input_json)
        return "string"

    def close(self, config_handle: int, *args, **kwargs) -> None:
        self.fake_g2config(config_handle)

    def create(self, *args, **kwargs) -> int:
        self.fake_g2config()
        return 0

    def delete_data_source(
        self, config_handle: int, input_json: str, *args, **kwargs
    ) -> None:
        self.fake_g2config(config_handle, input_json)

    def destroy(self, *args, **kwargs) -> None:
        self.fake_g2config()

    def init(
        self, module_name: str, ini_params: str, verbose_logging: int, *args, **kwargs
    ) -> None:
        self.fake_g2config(module_name, ini_params, verbose_logging)

    def list_data_sources(self, config_handle: int, *args, **kwargs) -> str:
        self.fake_g2config(config_handle)
        return "string"

    def load(self, json_config: str, *args, **kwargs) -> int:
        self.fake_g2config(json_config)
        return 0

    def save(self, config_handle: int, *args, **kwargs) -> str:
        self.fake_g2config(config_handle)
        return "string"
