#! /usr/bin/env python3

"""
TODO: g2product.py
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

# __all__ = ['G2Product']
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2023-10-30'
__updated__ = '2023-10-30'

SENZING_PRODUCT_ID = "5046"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md

# -----------------------------------------------------------------------------
# G2Product class
# -----------------------------------------------------------------------------


class G2Product:
    """
    G2 product module access library
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

    def fake_g2config(self, *args, **kwargs):
        """TODO: Remove once SDK methods have been implemented."""
        if len(args) + len(kwargs) > 2000:
            print(self.noop)

    # -------------------------------------------------------------------------
    # G2Product methods
    # -------------------------------------------------------------------------

    def destroy(self):
        """TODO: document"""
        self.fake_g2config()

    def init(self, module_name, ini_params, verbose_logging):
        """TODO: document"""
        self.fake_g2config(module_name, ini_params, verbose_logging)

    def license(self):
        """TODO: document"""
        self.fake_g2config()
        return "string"

    def version(self):
        """TODO: document"""
        self.fake_g2config()
        return "string"
