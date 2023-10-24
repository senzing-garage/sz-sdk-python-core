#! /usr/bin/env python3

"""
TODO: g2diagnostic.py
"""

# Import from standard library. https://docs.python.org/3/library/

import ctypes
import os
import threading
from typing import Any

from .g2diagnostic_abstract import G2DiagnosticAbstract
from .g2exception import G2Exception, translate_exception
from .g2helpers import as_normalized_int, as_normalized_string

# Import from https://pypi.org/

# Import from Senzing.


# Metadata

__all__ = ["G2Diagnostic"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

SENZING_PRODUCT_ID = "5042"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md


# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------


def find_file_in_path(filename: str) -> str:
    """Find a file in the PATH environment variable"""
    path_dirs = os.environ["PATH"].split(os.pathsep)
    for path_dir in path_dirs:
        file_path = os.path.join(path_dir, filename)
        if os.path.exists(file_path):
            return file_path
    return ""


class G2diagnosticGetdbinfoResult(ctypes.Structure):
    """In golang_helpers.h G2Diagnostic_getDBInfo_result"""

    # pylint: disable=R0903
    _fields_ = [("response", ctypes.c_char_p), ("returnCode", ctypes.c_longlong)]


# -----------------------------------------------------------------------------
# Utility classes
# -----------------------------------------------------------------------------


class ErrorBuffer(threading.local):
    """Buffer to call C"""

    # pylint: disable=R0903

    def __init__(self) -> None:
        super().__init__()
        self.string_buffer = ctypes.create_string_buffer(65535)
        self.string_buffer_size = ctypes.sizeof(self.string_buffer)


ERROR_BUFFER = ErrorBuffer()


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
    # Helper methods
    # -------------------------------------------------------------------------

    def determine_exception(self, *args: Any, **kwargs: Any) -> Exception:
        """Construct the Exception."""
        self.library_handle.G2Diagnostic_getLastException(
            ERROR_BUFFER.string_buffer, ctypes.sizeof(ERROR_BUFFER.string_buffer)
        )
        print(">>>>>>", ERROR_BUFFER.string_buffer.value)
        return Exception(translate_exception(str(ERROR_BUFFER.string_buffer.value)))

    # -------------------------------------------------------------------------
    # G2Diagnostic methods
    # -------------------------------------------------------------------------

    def check_db_perf(self, seconds_to_run: int, *args: Any, **kwargs: Any) -> str:
        self.fake_g2diagnostic(seconds_to_run)
        return "string"

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        self.fake_g2diagnostic()

    def get_available_memory(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2diagnostic()
        return 0

    def get_db_info(self, *args: Any, **kwargs: Any) -> str:
        # print(">>>> enter get_db_info")
        # self.library_handle.G2Diagnostic_getDBInfo_helper.argtypes = []
        # self.library_handle.G2Diagnostic_getDBInfo_helper.restype = ctypes.POINTER(
        #     G2diagnosticGetdbinfoResult
        # )
        # print(">>>> 1 get_db_info")

        # g2diagnostic_get_db_info_result = (
        #     self.library_handle.G2Diagnostic_getDBInfo_helper()
        # )
        # print(">>>> 2 get_db_info")

        # pprint(inspect.getmembers(g2diagnostic_get_db_info_result))
        # print(">>>> 2.1 get_db_info")

        # pprint(inspect.getmembers(g2diagnostic_get_db_info_result.contents))

        # print(vars(g2diagnostic_get_db_info_result))
        # print(">>>> 3 get_db_info")

        # address = self.library_handle.G2Diagnostic_getDBInfo_helper()

        # print("address:", type(address))
        # p = G2diagnosticGetdbinfoResult.from_address(address)
        # print("p", type(p))
        # print(p.returnCode)

        # p = G2diagnosticGetdbinfoResult.from_address()
        # _result = self.library_handle.G2Diagnostic_getDBInfo_helper()
        # result = _result.response
        # print(">>>>>>", result)
        # return "mjd was here"
        self.fake_g2diagnostic()
        return "string"

    def get_logical_cores(self, *args: Any, **kwargs: Any) -> int:
        self.library_handle.G2Diagnostic_getLogicalCores.argtypes = []
        return int(self.library_handle.G2Diagnostic_getLogicalCores())

    def get_physical_cores(self, *args: Any, **kwargs: Any) -> int:
        self.library_handle.G2Diagnostic_getPhysicalCores.argtypes = []
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
        self.library_handle.G2Diagnostic_init.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_int,
        ]
        result = self.library_handle.G2Diagnostic_init(
            as_normalized_string(module_name),
            as_normalized_string(ini_params),
            as_normalized_int(verbose_logging),
        )
        if result < 0:
            raise self.determine_exception()

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
