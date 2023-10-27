#! /usr/bin/env python3

"""
TODO: g2diagnostic.py
"""

# Import from standard library. https://docs.python.org/3/library/

import ctypes
import datetime
import json
import os
import threading
from typing import Any

from .g2diagnostic_abstract import G2DiagnosticAbstract
from .g2exception import EXCEPTION_MAP, G2Exception
from .g2helpers import as_normalized_int, as_normalized_string

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


# -----------------------------------------------------------------------------
# Utility classes
# -----------------------------------------------------------------------------


class G2diagnosticGetdbinfoResult(ctypes.Structure):
    """In golang_helpers.h G2Diagnostic_getDBInfo_result"""

    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]


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

        try:
            self.init(self.module_name, self.ini_params, self.verbose_logging)
        except Exception as error:
            # print(error)
            raise error

        # ----------------------------------------------------------------------
        # Initialize C function input parameters and results
        # ----------------------------------------------------------------------

        self.library_handle.G2Diagnostic_getDBInfo_helper.argtypes = []
        self.library_handle.G2Diagnostic_getDBInfo_helper.restype = (
            G2diagnosticGetdbinfoResult
        )
        self.library_handle.G2Diagnostic_getLogicalCores.argtypes = []
        self.library_handle.G2Diagnostic_getPhysicalCores.argtypes = []
        self.library_handle.G2GoHelper_free.argtypes = [ctypes.c_char_p]

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

    # def determine_exception(self, *args: Any, **kwargs: Any) -> Exception:
    #     """Construct the Exception."""
    #     self.library_handle.G2Diagnostic_getLastException(
    #         ERROR_BUFFER.string_buffer, ctypes.sizeof(ERROR_BUFFER.string_buffer)
    #     )
    #     print(">>>>>>", ERROR_BUFFER.string_buffer.value)
    #     return Exception(translate_exception(str(ERROR_BUFFER.string_buffer.value)))

    def get_message_level(self, error_id: int) -> str:
        """Determine the severity of the error"""
        # TODO: Implement
        return "WARN"

    def get_message_text(self, error_id: int, *args: Any) -> str:
        """Format the message text from a template and variables"""
        return self.ID_MESSAGES.get(
            error_id, f"No message for index {error_id}."
        ).format(*args)

    # def get_senzing_error(self) -> str:
    #     """Get the error from the Senzing engine."""
    #     self.library_handle.G2Diagnostic_getLastException(
    #         ERROR_BUFFER.string_buffer, ctypes.sizeof(ERROR_BUFFER.string_buffer)
    #     )
    #     self.library_handle.G2Diagnostic_clearLastException()

    #     print(">>>> type", type(ERROR_BUFFER.string_buffer.value))
    #     return str(ERROR_BUFFER.string_buffer.value)

    def get_senzing_error_text(self) -> str:
        """Given an exception of varying types, return an exception string."""

        self.library_handle.G2Diagnostic_getLastException(
            ERROR_BUFFER.string_buffer, ctypes.sizeof(ERROR_BUFFER.string_buffer)
        )
        self.library_handle.G2Diagnostic_clearLastException()
        exception = ERROR_BUFFER.string_buffer.value

        if exception is None:
            result = ""
        elif isinstance(exception, bytearray):
            result = exception.decode()
        elif isinstance(exception, bytes):
            result = exception.decode()
        elif isinstance(exception, Exception):
            result = str(exception).split(":", 1)[1].strip()
        else:
            result = exception
        assert isinstance(result, str)
        return result

    def get_senzing_error_code(self, error_text: str) -> int:
        """Given an exception string, find the exception code."""
        exception_message_splits = error_text.split("|", 1)
        result = int(exception_message_splits[0].strip().rstrip("EIW"))
        assert isinstance(result, int)
        return result

    def new_exception(self, error_id: int, *args: Any) -> Exception:
        """Generate a new exception based on the error_id."""

        senzing_error_text = self.get_senzing_error_text()
        senzing_error_code = self.get_senzing_error_code(senzing_error_text)
        message = {
            "time": datetime.datetime.utcnow().isoformat("T"),
            "text": self.get_message_text(error_id, *args),
            "level": self.get_message_level(error_id),
            "id": f"senzing-{SENZING_PRODUCT_ID}{error_id:4d}",
            "location": "",
            "status": "",
            "errorCode": senzing_error_code,
            "errors": senzing_error_text,
            "details": args,
        }

        # print(">>>> new_exception 2", message)

        senzing_error_class = EXCEPTION_MAP.get(senzing_error_code, G2Exception)
        # print(">>>> new_exception 3", type(senzing_error_class(json.dumps(message))))
        # print(">>>> new_exception 4", type(senzing_error_class))
        # print(">>>> new_exception 5", type(senzing_error_class()))
        # print(">>>> new_exception 6", senzing_error_class())

        # new_error = senzing_error_class(json.dumps(message))
        # new_error = senzing_error_class("BOB WAS HERE")

        # print(">>>> new_exception 7", new_error)
        # return Exception(json.dumps(message))
        return senzing_error_class(json.dumps(message))

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
        result = self.library_handle.G2Diagnostic_getDBInfo_helper()
        try:
            # raise self.new_exception(4007, result.return_code)

            if result.return_code != 0:
                raise self.new_exception(4007, result.return_code)
            # result_response = str(ctypes.cast(result.response, ctypes.c_char_p).value)
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
        self.library_handle.G2Diagnostic_init.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_int,
        ]

        result = 0

        try:
            result = self.library_handle.G2Diagnostic_init(
                as_normalized_string(module_name),
                as_normalized_string(ini_params),
                as_normalized_int(verbose_logging),
            )
        except Exception as e:
            print(">>>> init 999", e)

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
