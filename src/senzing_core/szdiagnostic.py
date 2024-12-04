"""
The `szdiagnostic` package is used to inspect the Senzing environment.
It is a wrapper over Senzing's SzDiagnostic C binding.
It conforms to the interface specified in
`szdiagnostic_abstract.py <https://github.com/senzing-garage/sz-sdk-python-core/blob/main/src/senzing_abstract/szdiagnostic_abstract.py>`_

To use szdiagnostic,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/er/lib
"""

# pylint: disable=R0903

from ctypes import POINTER, Structure, c_char, c_char_p, c_int, c_longlong, c_void_p
from functools import partial
from typing import Any, Dict, Union

from senzing import SzDiagnostic as SzDiagnosticAbstract

from ._helpers import (
    FreeCResources,
    as_c_char_p,
    as_python_str,
    as_str,
    catch_non_sz_exceptions,
    check_result_rc,
    load_sz_library,
)
from ._version import is_supported_senzingapi_version

# Metadata

__all__ = ["SzDiagnostic"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-27"


# -----------------------------------------------------------------------------
# Classes that are result structures from calls to Senzing
# -----------------------------------------------------------------------------


class SzResponseReturnCodeResult(Structure):
    """Simple response, return_code structure"""

    _fields_ = [
        ("response", POINTER(c_char)),
        ("return_code", c_longlong),
    ]


class SzDiagnosticCheckDatastorePerformanceResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h SzDiagnostic_checkDatastorePerformance_result"""


class SzDiagnosticGetDatastoreInfoResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h SzDiagnostic_getDatastoreInfo_result"""


class SzDiagnosticGetFeatureResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h SzDiagnostic_getFeature_result"""


# -----------------------------------------------------------------------------
# SzDiagnostic class
# -----------------------------------------------------------------------------


class SzDiagnostic(SzDiagnosticAbstract):
    """
    Use SzAbstractFactory.create_diagnostic() to create an SzDiagnostic object.
    The SzDiagnostic object uses the parameters provided to the SzAbstractFactory()
    function.

    Example:

    .. code-block:: python

        sz_abstract_factory = SzAbstractFactory(instance_name, settings)
        sz_diagnostic = sz_abstract_factory.create_diagnostic()

    Parameters:

    Raises:

    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(self, **kwargs: Any) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """

        _ = kwargs

        # Determine if Senzing API version is acceptable.
        is_supported_senzingapi_version()

        # Load binary library.
        self.library_handle = load_sz_library()

        # Partial function to use this modules self.library_handle for exception handling
        self.check_result = partial(
            check_result_rc,
            self.library_handle.SzDiagnostic_getLastException,
            self.library_handle.SzDiagnostic_clearLastException,
            self.library_handle.SzDiagnostic_getLastExceptionCode,
        )

        # Initialize C function input parameters and results.
        # Must be synchronized with er/sdk/c/libSzDiagnostic.h

        self.library_handle.SzDiagnostic_checkDatastorePerformance_helper.argtypes = [c_longlong]
        self.library_handle.SzDiagnostic_checkDatastorePerformance_helper.restype = (
            SzDiagnosticCheckDatastorePerformanceResult
        )
        self.library_handle.SzDiagnostic_destroy.argtypes = []
        self.library_handle.SzDiagnostic_destroy.restype = c_longlong
        self.library_handle.SzDiagnostic_getDatastoreInfo_helper.argtypes = []
        self.library_handle.SzDiagnostic_getDatastoreInfo_helper.restype = SzDiagnosticGetDatastoreInfoResult
        self.library_handle.SzDiagnostic_getFeature_helper.argtypes = [c_longlong]
        self.library_handle.SzDiagnostic_getFeature_helper.restype = SzDiagnosticGetFeatureResult
        self.library_handle.SzDiagnostic_init.argtypes = [c_char_p, c_char_p, c_int]
        self.library_handle.SzDiagnostic_init.restype = c_longlong
        self.library_handle.SzDiagnostic_initWithConfigID.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.SzDiagnostic_initWithConfigID.restype = c_longlong
        self.library_handle.SzDiagnostic_reinit.argtypes = [c_longlong]
        self.library_handle.SzDiagnostic_reinit.restype = c_longlong
        self.library_handle.SzHelper_free.argtypes = [c_void_p]

    def __del__(self) -> None:
        """Destructor"""

    # -------------------------------------------------------------------------
    # SzDiagnostic methods
    # -------------------------------------------------------------------------

    @catch_non_sz_exceptions
    def check_datastore_performance(self, seconds_to_run: int) -> str:
        result = self.library_handle.SzDiagnostic_checkDatastorePerformance_helper(seconds_to_run)
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    def _destroy(self) -> None:
        _ = self.library_handle.SzDiagnostic_destroy()

    def get_datastore_info(self) -> str:
        result = self.library_handle.SzDiagnostic_getDatastoreInfo_helper()
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    # NOTE This is included but not to be documented, used by sz_explorer
    @catch_non_sz_exceptions
    def get_feature(self, feature_id: int) -> str:
        result = self.library_handle.SzDiagnostic_getFeature_helper(feature_id)
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    @catch_non_sz_exceptions
    def _initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        config_id: int = 0,
        verbose_logging: int = 0,
    ) -> None:
        if config_id == 0:
            result = self.library_handle.SzDiagnostic_init(
                as_c_char_p(instance_name),
                as_c_char_p(as_str(settings)),
                verbose_logging,
            )
            self.check_result(result)
            return

        result = self.library_handle.SzDiagnostic_initWithConfigID(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            config_id,
            verbose_logging,
        )
        self.check_result(result)

    def purge_repository(self) -> None:
        result = self.library_handle.SzDiagnostic_purgeRepository()
        self.check_result(result)

    @catch_non_sz_exceptions
    def _reinitialize(self, config_id: int) -> None:
        result = self.library_handle.SzDiagnostic_reinit(config_id)
        self.check_result(result)
