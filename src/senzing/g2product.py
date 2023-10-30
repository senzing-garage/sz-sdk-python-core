"""
TODO: g2product.py
"""

import ctypes
import os
from typing import Any

from .g2exception import G2Exception, new_g2exception
from .g2helpers import as_normalized_int, as_normalized_string, find_file_in_path
from .g2product_abstract import G2ProductAbstract

# Metadata

__all__ = ["G2Product"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

SENZING_PRODUCT_ID = "5046"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md
CALLER_SKIP = 6  # Number of stack frames to skip when reporting location in Exception.

# -----------------------------------------------------------------------------
# G2Product class
# -----------------------------------------------------------------------------


class G2Product(G2ProductAbstract):
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
        **kwargs: Any,
    ) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """

        self.ini_params = ini_params
        self.module_name = module_name
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

        # Initialize C function input parameters and results
        # Must be synchronized with g2/sdk/c/libg2product.h

        self.library_handle.G2GoHelper_free.argtypes = [ctypes.c_char_p]

        self.library_handle.G2Product_clearLastException.argtypes = []
        self.library_handle.G2Product_clearLastException.restype = None
        self.library_handle.G2Product_destroy.argtypes = []
        self.library_handle.G2Product_destroy.restype = ctypes.c_longlong
        self.library_handle.G2Product_getLastException.argtypes = [
            ctypes.POINTER(ctypes.c_char),
            ctypes.c_size_t,
        ]
        self.library_handle.G2Product_getLastException.restype = ctypes.c_longlong
        self.library_handle.G2Product_init.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_int,
        ]
        self.library_handle.G2Product_init.restype = ctypes.c_longlong
        self.library_handle.G2Product_license.argtypes = []
        self.library_handle.G2Product_license.restype = ctypes.c_char_p
        self.library_handle.G2Product_version.argtypes = []
        self.library_handle.G2Product_version.restype = ctypes.c_char_p

        # Initialize Senzing engine.

        self.init(self.module_name, self.ini_params, self.verbose_logging)

    def __del__(self) -> None:
        """Destructor"""
        self.destroy()

    # -------------------------------------------------------------------------
    # Exception helpers
    # -------------------------------------------------------------------------

    def new_exception(self, error_id: int, *args: Any) -> Exception:
        """
        Generate a new exception based on the error_id.

        :meta private:
        """
        return new_g2exception(
            self.library_handle.G2Product_getLastException,
            self.library_handle.G2Product_clearLastException,
            SENZING_PRODUCT_ID,
            error_id,
            self.ID_MESSAGES,
            CALLER_SKIP,
            *args,
        )

    # -------------------------------------------------------------------------
    # G2Product methods
    # -------------------------------------------------------------------------

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        result = self.library_handle.G2Product_destroy()
        if result != 0:
            raise self.new_exception(4001, result)

    def init(
        self,
        module_name: str,
        ini_params: str,
        verbose_logging: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        result = self.library_handle.G2Product_init(
            as_normalized_string(module_name),
            as_normalized_string(ini_params),
            as_normalized_int(verbose_logging),
        )
        if result < 0:
            raise self.new_exception(
                4003, module_name, ini_params, verbose_logging, result
            )

    def license(self, *args: Any, **kwargs: Any) -> str:
        return str(self.library_handle.G2Product_license().decode())

    def version(self, *args: Any, **kwargs: Any) -> str:
        return str(self.library_handle.G2Product_version().decode())
