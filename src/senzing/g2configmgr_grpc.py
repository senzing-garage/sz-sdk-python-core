#! /usr/bin/env python3

"""
TODO: g2configmgr_grpc.py
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
from .g2configmgr_abstract import G2ConfigMgrAbstract

# Metadata

__all__ = ["G2ConfigMgrGrpc"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

SENZING_PRODUCT_ID = "5051"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md

# -----------------------------------------------------------------------------
# G2ConfigMgrGrpc class
# -----------------------------------------------------------------------------


class G2ConfigMgrGrpc(G2ConfigMgrAbstract):
    """
    G2 config-manager module access library
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self, module_name, ini_params, verbose_logging, *args, **kwargs
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

    def __del__(self):
        """Destructor"""
        self.destroy()

    # -------------------------------------------------------------------------
    # Development methods - to be removed after initial development
    # -------------------------------------------------------------------------

    def fake_g2configmgr(self, *args, **kwargs):
        """TODO: Remove once SDK methods have been implemented."""
        if len(args) + len(kwargs) > 2000:
            print(self.noop)

    # -------------------------------------------------------------------------
    # G2ConfigMgr methods
    # -------------------------------------------------------------------------

    def add_config(self, config_str: str, config_comments: str, *args, **kwargs) -> int:
        self.fake_g2configmgr(config_str, config_comments)
        return 0

    def destroy(self, *args, **kwargs) -> None:
        self.fake_g2configmgr()

    def get_config(self, config_id: int, *args, **kwargs) -> str:
        self.fake_g2configmgr(config_id)
        return "string"

    def get_config_list(self, *args, **kwargs) -> str:
        self.fake_g2configmgr()
        return "string"

    def get_default_config_id(self, *args, **kwargs) -> int:
        self.fake_g2configmgr()
        return 0

    def init(
        self, module_name: str, ini_params: str, verbose_logging: int, *args, **kwargs
    ) -> None:
        self.fake_g2configmgr(module_name, ini_params, verbose_logging)

    def replace_default_config_id(
        self, old_config_id: int, new_config_id: int, *args, **kwargs
    ) -> None:
        self.fake_g2configmgr(old_config_id, new_config_id)

    def set_default_config_id(self, config_id: int, *args, **kwargs) -> None:
        self.fake_g2configmgr(config_id)
