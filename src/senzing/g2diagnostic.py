#! /usr/bin/env python3

"""
TODO: g2diagnostic.py
"""

import ctypes
import os
from typing import Any

from .g2diagnostic_abstract import G2DiagnosticAbstract
from .g2exception import G2Exception, new_g2exception
from .g2helpers import as_normalized_int, as_normalized_string, find_file_in_path

# Metadata

__all__ = ["G2Diagnostic"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

SENZING_PRODUCT_ID = "5042"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md
CALLER_SKIP = 6

# -----------------------------------------------------------------------------
# Classes that are result structures from calls to Senzing
# -----------------------------------------------------------------------------


class G2diagnosticGetdbinfoResult(ctypes.Structure):
    """In golang_helpers.h G2Diagnostic_getDBInfo_result"""

    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]


class G2diagnosticCheckDBPerfResult(ctypes.Structure):
    """In golang_helpers.h G2Diagnostic_getDBInfo_result"""

    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]


# -----------------------------------------------------------------------------
# G2Diagnostic class
# -----------------------------------------------------------------------------


class G2Diagnostic(G2DiagnosticAbstract):
    """
    G2 config module access library
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
        **kwargs: Any,
    ) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """

        self.ini_params = ini_params
        self.module_name = module_name
        self.noop = ""
        self.verbose_logging = verbose_logging

        try:
            if os.name == "nt":
                self.library_handle = ctypes.cdll.LoadLibrary(
                    find_file_in_path("G2.dll")
                )
            else:
                self.library_handle = ctypes.cdll.LoadLibrary("libG2.so")
        except OSError as err:
            raise G2Exception("Failed to load the G2 library") from err

        # Initialize C function input parameters and results.
        # Must be synchronized with g2/sdk/c/libg2diagnostic.h

        self.library_handle.G2Diagnostic_checkDBPerf_helper.restype = (
            G2diagnosticCheckDBPerfResult
        )
        self.library_handle.G2Diagnostic_clearLastException.argtypes = []
        self.library_handle.G2Diagnostic_clearLastException.restype = None
        self.library_handle.G2Diagnostic_getDBInfo_helper.argtypes = []
        self.library_handle.G2Diagnostic_getDBInfo_helper.restype = (
            G2diagnosticGetdbinfoResult
        )
        self.library_handle.G2Diagnostic_getLastException.argtypes = [
            ctypes.POINTER(ctypes.c_char),
            ctypes.c_size_t,
        ]
        self.library_handle.G2Diagnostic_getLastException.restype = ctypes.c_longlong
        self.library_handle.G2Diagnostic_getLogicalCores.argtypes = []
        self.library_handle.G2Diagnostic_getPhysicalCores.argtypes = []
        self.library_handle.G2Diagnostic_init.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_int,
        ]
        self.library_handle.G2GoHelper_free.argtypes = [ctypes.c_char_p]

        # Initialize Senzing engine.

        self.init(self.module_name, self.ini_params, self.verbose_logging)

    def __del__(self) -> None:
        """Destructor"""
        self.destroy()

    # -------------------------------------------------------------------------
    # Development methods - to be removed after initial development
    # -------------------------------------------------------------------------

    def fake_g2diagnostic(self, *args: Any, **kwargs: Any) -> None:
        """
        TODO: Remove once SDK methods have been implemented.

        :meta private:
        """
        if len(args) + len(kwargs) > 2000:
            print(self.noop)

    # -------------------------------------------------------------------------
    # Exception helpers
    # -------------------------------------------------------------------------

    def new_exception(self, error_id: int, *args: Any) -> Exception:
        """
        Generate a new exception based on the error_id.

        :meta private:
        """
        return new_g2exception(
            self.library_handle.G2Diagnostic_getLastException,
            self.library_handle.G2Diagnostic_clearLastException,
            SENZING_PRODUCT_ID,
            error_id,
            self.ID_MESSAGES,
            CALLER_SKIP,
            *args,
        )

    # -------------------------------------------------------------------------
    # G2Diagnostic methods
    # -------------------------------------------------------------------------

    def check_db_perf(self, seconds_to_run: int, *args: Any, **kwargs: Any) -> str:
        # self.fake_g2diagnostic(seconds_to_run)
        # return "string"
        result = self.library_handle.G2Diagnostic_checkDBPerf_helper(seconds_to_run)
        try:
            if result.return_code != 0:
                raise self.new_exception(4007, result.return_code)
            result_response = ctypes.cast(result.response, ctypes.c_char_p).value
            result_response_str = result_response.decode() if result_response else ""
        finally:
            self.library_handle.G2GoHelper_free(result.response)
        return result_response_str

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        self.fake_g2diagnostic()

    def get_available_memory(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2diagnostic()
        return 0

    def get_db_info(self, *args: Any, **kwargs: Any) -> str:
        result = self.library_handle.G2Diagnostic_getDBInfo_helper()
        try:
            if result.return_code != 0:
                raise self.new_exception(4007, result.return_code)
            result_response = ctypes.cast(result.response, ctypes.c_char_p).value
            result_response_str = result_response.decode() if result_response else ""
        finally:
            self.library_handle.G2GoHelper_free(result.response)
        return result_response_str

    def get_logical_cores(self, *args: Any, **kwargs: Any) -> int:
        return int(self.library_handle.G2Diagnostic_getLogicalCores())

    def get_physical_cores(self, *args: Any, **kwargs: Any) -> int:
        return int(self.library_handle.G2Diagnostic_getPhysicalCores())

    def get_total_system_memory(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2diagnostic()
        return 0

    def init(
        self,
        module_name: str,
        ini_params: str,
        verbose_logging: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        result = self.library_handle.G2Diagnostic_init(
            as_normalized_string(module_name),
            as_normalized_string(ini_params),
            as_normalized_int(verbose_logging),
        )
        if result < 0:
            raise self.new_exception(
                4018, module_name, ini_params, verbose_logging, result
            )

    def init_with_config_id(
        self,
        module_name: str,
        ini_params: str,
        init_config_id: int,
        verbose_logging: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.fake_g2diagnostic(module_name, ini_params, init_config_id, verbose_logging)

    def reinit(self, init_config_id: int, *args: Any, **kwargs: Any) -> None:
        self.fake_g2diagnostic(init_config_id)
