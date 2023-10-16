#! /usr/bin/env python3

"""
TODO: g2configmgr.py
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

# Metadata

# __all__ = ['g2configmgr']
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2023-10-30'
__updated__ = '2023-10-30'

SENZING_PRODUCT_ID = "5041"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md

# -----------------------------------------------------------------------------
# G2ConfigMgr class
# -----------------------------------------------------------------------------


class G2ConfigMgr:
    """
    G2 config-manager module access library
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(self, module_name, ini_params, verbose_logging):
        """Constructor"""

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

    def add_config(self, config_str: str, config_comments: str) -> int:
        """TODO: document"""
        self.fake_g2configmgr(config_str, config_comments)
        return "int64"

    def destroy(self) -> None:
        """TODO: document"""
        self.fake_g2configmgr()

    def get_config(self, config_id: int) -> str:
        """TODO: document"""
        self.fake_g2configmgr(config_id)
        return "string"

    def get_config_list(self) -> str:
        """TODO: document"""
        self.fake_g2configmgr()
        return "string"

    def get_default_config_id(self) -> int:
        """TODO: document"""
        self.fake_g2configmgr()
        return "int64"

    def init(self, module_name: str, ini_params: str, verbose_logging: int) -> None:
        """TODO: document"""
        self.fake_g2configmgr(module_name, ini_params, verbose_logging)

    def replace_default_config_id(self, old_config_id: int, new_config_id: int) -> None:
        """TODO: document"""
        self.fake_g2configmgr(old_config_id, new_config_id)

    def set_default_config_id(self, config_id: int) -> None:
        """TODO: document"""
        self.fake_g2configmgr(config_id)
