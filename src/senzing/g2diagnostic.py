#! /usr/bin/env python3

"""
g2diagnostic.py
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

# __all__ = ['g2diagnostic']
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2023-10-30'
__updated__ = '2023-10-30'

SENZING_PRODUCT_ID = "5042"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md

# -----------------------------------------------------------------------------
# G2Config class
# -----------------------------------------------------------------------------


class G2Diagnostic:
    """
    G2 config module access library
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

    def fake_g2diagnostic(self, *args, **kwargs):
        """TODO: Remove once SDK methods have been implemented."""
        if len(args) + len(kwargs) > 2000:
            print(self.noop)

    # -------------------------------------------------------------------------
    # G2Diagnostic methods
    # -------------------------------------------------------------------------

    def check_db_perf(self, seconds_to_run):
        """TODO: document"""
        self.fake_g2diagnostic(seconds_to_run)
        return "string"

    def destroy(self):
        """TODO: document"""
        self.fake_g2diagnostic()

    def get_available_memory(self):
        """TODO: document"""
        self.fake_g2diagnostic()
        return "int64"

    def get_db_info(self):
        """TODO: document"""
        self.fake_g2diagnostic()
        return "string"

    def get_logical_cores(self):
        """TODO: document"""
        self.fake_g2diagnostic()
        return "int"

    def get_phhysical_cores(self):
        """TODO: document"""
        self.fake_g2diagnostic()
        return "int"

    def get_total_system_memory(self):
        """TODO: document"""
        self.fake_g2diagnostic()
        return "int64"

    def init(self, module_name, ini_params, verbose_logging):
        """TODO: document"""
        self.fake_g2diagnostic(module_name, ini_params, verbose_logging)

    def init_with_config_id(self, module_name, ini_params, init_config_id, verbose_logging):
        """TODO: document"""
        self.fake_g2diagnostic(module_name, ini_params, init_config_id, verbose_logging)

    def reinit(self, init_config_id):
        """TODO: document"""
        self.fake_g2diagnostic(init_config_id)
