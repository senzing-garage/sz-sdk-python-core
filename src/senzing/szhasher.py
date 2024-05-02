#! /usr/bin/env python3

"""
TODO: szhasher.py
"""

import os
from ctypes import POINTER, c_char, c_longlong, c_size_t, cdll
from types import TracebackType
from typing import Any, Type, Union

from senzing import SzError, SzHasherAbstract, find_file_in_path, new_szexception

from .szversion import is_supported_senzingapi_version

# Metadata

__all__ = ["SzHasher"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-07"

SENZING_PRODUCT_ID = "5045"  # See https://github.com/senzing-garage/knowledge-base/blob/main/lists/senzing-component-ids.md
CALLER_SKIP = 6

# -----------------------------------------------------------------------------
# Classes that are result structures from calls to Senzing
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# G2Hasher class
# -----------------------------------------------------------------------------


class SzHasher(SzHasherAbstract):
    """
    G2 product module access library
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        instance_name: str = "",
        settings: str = "",
        config_id: int = 0,
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """
        # pylint: disable=W0613

        # Verify parameters.

        if (len(instance_name) == 0) or (len(settings) == 0):
            if len(instance_name) + len(settings) != 0:
                raise self.new_exception(9999, instance_name, settings)

        self.settings = settings
        self.config_id = config_id
        self.instance_name = instance_name
        self.noop = ""
        self.verbose_logging = verbose_logging

        # Determine if Senzing API version is acceptable.

        is_supported_senzingapi_version()

        # Load binary library.

        try:
            if os.name == "nt":
                self.library_handle = cdll.LoadLibrary(
                    find_file_in_path("G2Hasher.dll")
                )
            else:
                self.library_handle = cdll.LoadLibrary("libG2Hasher.so")
        except OSError as err:
            raise SzError("Failed to load the G2 library") from err

        # Initialize C function input parameters and results.
        # Must be synchronized with g2/sdk/c/libg2hasher.h

        self.library_handle.G2Hasher_clearLastException.argtypes = []
        self.library_handle.G2Hasher_clearLastException.restype = None
        # self.library_handle.G2Hasher_destroy.argtypes = []
        # self.library_handle.G2Hasher_destroy.restype = c_longlong
        # self.library_handle.G2Hasher_exportTokenLibrary.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Hasher_exportTokenLibrary.restype = c_longlong
        self.library_handle.G2Hasher_getLastException.argtypes = [
            POINTER(c_char),
            c_size_t,
        ]
        self.library_handle.G2Hasher_getLastException.restype = c_longlong
        # self.library_handle.G2Hasher_getLastExceptionCode.argtypes = []
        # self.library_handle.G2Hasher_getLastExceptionCode.restype = c_longlong
        # self.library_handle.G2Hasher_init.argtypes = [c_char_p, c_char_p, c_int]
        # self.library_handle.G2Hasher_init.restype = c_longlong
        # self.library_handle.G2Hasher_initWithConfig.argtypes = [c_char_p, c_char_p, c_char_p, c_int]
        # self.library_handle.G2Hasher_initWithConfig.restype = c_longlong
        # self.library_handle.G2Hasher_process.argtypes = [c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Hasher_process.restype = c_longlong

        # Initialize Senzing engine.

        if len(instance_name) > 0:
            self.init(self.instance_name, self.settings, self.verbose_logging)

    def __del__(self) -> None:
        """Destructor"""
        try:
            self.destroy()
        except SzError:
            pass

    def __enter__(
        self,
    ) -> (
        Any
    ):  # TODO: Replace "Any" with "Self" once python 3.11 is lowest supported python version.
        """Context Manager method."""
        return self

    def __exit__(
        self,
        exc_type: Union[Type[BaseException], None],
        exc_val: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ) -> None:
        """Context Manager method."""

    # -------------------------------------------------------------------------
    # Development methods - to be removed after initial development
    # -------------------------------------------------------------------------

    def fake_szhasher(self, *args: Any, **kwargs: Any) -> None:
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
        return new_szexception(
            self.library_handle.G2Hasher_getLastException,
            self.library_handle.G2Hasher_clearLastException,
            SENZING_PRODUCT_ID,
            error_id,
            self.ID_MESSAGES,
            CALLER_SKIP,
            *args,
        )

    # -------------------------------------------------------------------------
    # G2Hasher methods
    # -------------------------------------------------------------------------

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        self.fake_szhasher()

    def export_token_library(self, *args: Any, **kwargs: Any) -> str:
        self.fake_szhasher()
        return "response"

    def init(
        self,
        instance_name: str,
        settings: str,
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        self.fake_szhasher(instance_name, settings, verbose_logging)

    def init_with_config_id(
        self,
        instance_name: str,
        settings: str,
        config_id: int,
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        self.fake_szhasher(instance_name, settings, config_id, verbose_logging)

    def process(self, record: str, *args: Any, **kwargs: Any) -> str:
        self.fake_szhasher(record)
        return "response"

    def reinit(self, init_config_id: int, *args: Any, **kwargs: Any) -> None:
        self.fake_szhasher(init_config_id)
