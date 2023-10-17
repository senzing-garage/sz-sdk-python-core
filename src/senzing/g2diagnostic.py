#! /usr/bin/env python3

"""
TODO: g2diagnostic.py
"""

# Import from standard library. https://docs.python.org/3/library/

from ctypes import cdll
# import functools
# import json
import os
# import threading
# import warnings

# Import from https://pypi.org/

# Import from Senzing.

from .g2exception import G2Exception
# from .g2exception import G2Exception, translate_exception

# Metadata

__all__ = ['G2Diagnostic']
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2023-10-30'
__updated__ = '2023-10-30'

SENZING_PRODUCT_ID = "5042"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md


# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------

def find_file_in_path(filename):
    """Find a file in the PATH environment variable"""
    path_dirs = os.environ['PATH'].split(os.pathsep)
    for path_dir in path_dirs:
        file_path = os.path.join(path_dir, filename)
        if os.path.exists(file_path):
            return file_path
    return None


# -----------------------------------------------------------------------------
# G2Diagnostic class
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

        try:
            if os.name == 'nt':
                self.library_handle = cdll.LoadLibrary(find_file_in_path("G2.dll"))
            else:
                self.library_handle = cdll.LoadLibrary("libG2.so")
        except OSError as err:
            raise G2Exception("Failed to load the G2 library") from err

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

    def check_db_perf(self, seconds_to_run: int) -> str:
        """TODO: document"""
        self.fake_g2diagnostic(seconds_to_run)
        return "string"

    def destroy(self) -> None:
        """TODO: document"""
        self.fake_g2diagnostic()

    def get_available_memory(self) -> int:
        """TODO: document"""
        self.fake_g2diagnostic()
        return "int64"

    def get_db_info(self) -> str:
        """TODO: document"""
        self.fake_g2diagnostic()
        return "string"

    def get_logical_cores(self) -> int:
        """TODO: document"""
        self.library_handle.G2Diagnostic_getLogicalCores.argtypes = []
        return self.library_handle.G2Diagnostic_getLogicalCores()

    def get_physical_cores(self) -> int:
        """TODO: document"""
        self.library_handle.G2Diagnostic_getPhysicalCores.argtypes = []
        return self.library_handle.G2Diagnostic_getPhysicalCores()

    def get_total_system_memory(self) -> int:
        """TODO: document"""
        self.fake_g2diagnostic()
        return "int64"

    def init(self, module_name: str, ini_params: str, verbose_logging: int) -> None:
        """TODO: document"""
        self.fake_g2diagnostic(module_name, ini_params, verbose_logging)

    def init_with_config_id(self, module_name: str, ini_params: str, init_config_id: int, verbose_logging: int) -> None:
        """TODO: document"""
        self.fake_g2diagnostic(module_name, ini_params, init_config_id, verbose_logging)

    def reinit(self, init_config_id: int) -> None:
        """TODO: document"""
        self.fake_g2diagnostic(init_config_id)
