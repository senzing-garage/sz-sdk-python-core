"""
``senzing_core.szdiagnostic.SzDiagnosticCore`` is an implementation
of the `senzing.szdiagnostic.SzDiagnostic`_ interface that communicates with the Senzing binaries.

To use szdiagnostic,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/er/lib

.. _senzing.szdiagnostic.SzDiagnostic: https://garage.senzing.com/sz-sdk-python/senzing.html#module-senzing.szdiagnostic
"""

# pylint: disable=R0903

from ctypes import POINTER, Structure, c_char, c_char_p, c_int, c_longlong, c_void_p
from functools import partial
from typing import Any, Dict, Union

from senzing import SzBadInputError, SzDiagnostic, SzNotInitializedError

from ._helpers import (
    FreeCResources,
    as_c_char_p,
    as_python_str,
    as_str,
    catch_sdk_exceptions,
    check_is_destroyed,
    check_result_rc,
    load_sz_library,
)

# Metadata

__all__ = ["SzDiagnosticCore"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2025-07-19"


# -----------------------------------------------------------------------------
# Classes that are result structures from calls to Senzing
# -----------------------------------------------------------------------------


class SzResponseReturnCodeResult(Structure):
    """Simple response, return_code structure"""

    _fields_ = [
        ("response", POINTER(c_char)),
        ("return_code", c_longlong),
    ]


class SzDiagnosticCheckRepositoryPerformanceResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h SzDiagnostic_checkRepositoryPerformance_result"""


class SzDiagnosticGetFeatureResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h SzDiagnostic_getFeature_result"""


class SzDiagnosticGetRepositoryInfoResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h SzDiagnostic_getRepositoryInfo_result"""


# -----------------------------------------------------------------------------
# SzDiagnosticCore class
# -----------------------------------------------------------------------------


class SzDiagnosticCore(SzDiagnostic):
    """
    Use SzAbstractFactoryCore.create_diagnostic() to create an SzDiagnostic object.
    The SzDiagnostic object uses the arguments provided to SzAbstractFactoryCore().

    Example:

    .. code-block:: python

        from senzing_core import SzAbstractFactoryCore

        sz_abstract_factory = SzAbstractFactoryCore(instance_name, settings)
        sz_diagnostic = sz_abstract_factory.create_diagnostic()

    Args:

    Raises:

    """

    # -------------------------------------------------------------------------
    # Dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(self, **kwargs: Any) -> None:
        _ = kwargs

        self._is_destroyed = False
        self._library_handle = load_sz_library()

        # Partial function to use this modules self._library_handle for exception handling
        self._check_result = partial(
            check_result_rc,
            self._library_handle.SzDiagnostic_getLastException,
            self._library_handle.SzDiagnostic_clearLastException,
            self._library_handle.SzDiagnostic_getLastExceptionCode,
        )

        # Initialize C function input parameters and results.
        # Must be synchronized with er/sdk/c/libSzDiagnostic.h
        self._library_handle.SzDiagnostic_checkRepositoryPerformance_helper.argtypes = [c_longlong]
        self._library_handle.SzDiagnostic_checkRepositoryPerformance_helper.restype = (
            SzDiagnosticCheckRepositoryPerformanceResult
        )
        self._library_handle.SzDiagnostic_destroy.argtypes = []
        self._library_handle.SzDiagnostic_destroy.restype = c_longlong
        self._library_handle.SzDiagnostic_getRepositoryInfo_helper.argtypes = []
        self._library_handle.SzDiagnostic_getFeature_helper.restype = SzDiagnosticGetFeatureResult
        self._library_handle.SzDiagnostic_getRepositoryInfo_helper.restype = SzDiagnosticGetRepositoryInfoResult
        self._library_handle.SzDiagnostic_getFeature_helper.argtypes = [c_longlong]
        self._library_handle.SzDiagnostic_init.argtypes = [c_char_p, c_char_p, c_int]
        self._library_handle.SzDiagnostic_init.restype = c_longlong
        self._library_handle.SzDiagnostic_initWithConfigID.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
            c_longlong,
        ]
        self._library_handle.SzDiagnostic_initWithConfigID.restype = c_longlong
        self._library_handle.SzDiagnostic_reinit.argtypes = [c_longlong]
        self._library_handle.SzDiagnostic_reinit.restype = c_longlong
        self._library_handle.SzHelper_free.argtypes = [c_void_p]

    @property
    def is_destroyed(self) -> bool:
        """Return if the instance has been destroyed."""
        return self._is_destroyed

    # -------------------------------------------------------------------------
    # SzDiagnostic methods
    # -------------------------------------------------------------------------

    @check_is_destroyed
    @catch_sdk_exceptions
    def check_repository_performance(self, seconds_to_run: int) -> str:
        result = self._library_handle.SzDiagnostic_checkRepositoryPerformance_helper(seconds_to_run)
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    # NOTE - Not to use check_is_destroyed decorator
    def _destroy(self) -> None:
        if not self._is_destroyed:
            _ = self._library_handle.SzDiagnostic_destroy()
            self._is_destroyed = True

    # NOTE - Internal use only!
    def _internal_only_destroy(self) -> None:
        result = self._library_handle.SzDiagnostic_destroy()
        self._check_result(result)

    @check_is_destroyed
    @catch_sdk_exceptions
    def get_feature(self, feature_id: int) -> str:
        result = self._library_handle.SzDiagnostic_getFeature_helper(feature_id)
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @check_is_destroyed
    def get_repository_info(self) -> str:
        result = self._library_handle.SzDiagnostic_getRepositoryInfo_helper()
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @check_is_destroyed
    @catch_sdk_exceptions
    def _initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        config_id: int = 0,
        verbose_logging: int = 0,
    ) -> None:
        if config_id == 0:
            result = self._library_handle.SzDiagnostic_init(
                as_c_char_p(instance_name),
                as_c_char_p(as_str(settings)),
                verbose_logging,
            )
            self._check_result(result)
            return

        result = self._library_handle.SzDiagnostic_initWithConfigID(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            config_id,
            verbose_logging,
        )
        self._check_result(result)

    # NOTE - Internal use only!
    def _internal_is_initialized(self) -> bool:
        try:
            _ = self.get_repository_info()
        except SzNotInitializedError:
            return False

        return True

    @check_is_destroyed
    def purge_repository(self) -> None:
        result = self._library_handle.SzDiagnostic_purgeRepository()
        self._check_result(result)

    @check_is_destroyed
    @catch_sdk_exceptions
    def _reinitialize(self, config_id: int) -> None:
        result = self._library_handle.SzDiagnostic_reinit(config_id)
        self._check_result(result)
