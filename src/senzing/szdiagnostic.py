"""
The `szdiagnostic` package is used to inspect the Senzing environment.
It is a wrapper over Senzing's SzDiagnostic C binding.
It conforms to the interface specified in
`szdiagnostic_abstract.py <https://github.com/senzing-garage/sz-sdk-python/blob/main/src/senzing_abstract/szdiagnostic_abstract.py>`_

To use szdiagnostic,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/er/lib
"""

# pylint: disable=R0903

from contextlib import suppress
from ctypes import POINTER, Structure, c_char, c_char_p, c_int, c_longlong
from functools import partial
from typing import Any, Dict, Union

from senzing import SzDiagnosticAbstract

from ._helpers import (
    FreeCResources,
    as_c_char_p,
    as_python_str,
    as_str,
    catch_exceptions,
    check_result_rc,
    load_sz_library,
    sdk_exception,
)
from ._version import is_supported_senzingapi_version

# Metadata

__all__ = ["SzDiagnostic"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-27"

# SENZING_PRODUCT_ID = "5042"  # See https://github.com/senzing-garage/knowledge-base/blob/main/lists/senzing-component-ids.md

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
    """In golang_helpers.h G2Diagnostic_checkDatastorePerformance_result"""


class SzDiagnosticGetDatastoreInfoResult(SzResponseReturnCodeResult):
    """In golang_helpers.h G2Diagnostic_getDatastoreInfo_result"""


class SzDiagnosticGetFeatureResult(SzResponseReturnCodeResult):
    """In golang_helpers.h G2Diagnostic_getFeature_result"""


# -----------------------------------------------------------------------------
# SzDiagnostic class
# -----------------------------------------------------------------------------


class SzDiagnostic(SzDiagnosticAbstract):
    # TODO - Ant - Correct the 'If the SzDiagnostic constructor is called without parameters,' and check other modules
    #            - Either `instance_name` and `settings` must both be specified or neither must be specified.?
    """
    The `initialize` method initializes the Senzing SzDiagnostic object.
    It must be called prior to any other calls.

    **Note:** If the SzDiagnostic constructor is called with parameters,
    the constructor will automatically call the `initialize()` method.

    Example:

    .. code-block:: python

        sz_diagnostic = SzDiagnostic(instance_name, settings)

    If the SzDiagnostic constructor is called without parameters,
    the `initialize()` method must be called to initialize the use of SzDiagnostic.

    Example:

    .. code-block:: python

        sz_diagnostic = SzDiagnostic()
        sz_diagnostic.initialize(instance_name, settings)

    Either `instance_name` and `settings` must both be specified or neither must be specified.
    Just specifying one or the other results in a **SzError**.

    Parameters:
        instance_name:
            `Optional:` A name for the auditing node, to help identify it within system logs. Default: ""
        settings:
            `Optional:` A JSON string containing configuration parameters. Default: ""
        config_id:
            `Optional:` Specify the ID of a specific Senzing configuration. Default: 0 - Use default Senzing configuration
        verbose_logging:
            `Optional:` A flag to enable deeper logging of the Sz processing. 0 for no Senzing logging; 1 for logging. Default: 0

    Raises:
        TypeError: Incorrect datatype detected on input parameter.
        SzError: Failed to load the Sz library or incorrect `instance_name`, `settings` combination.


    .. collapse:: Example:

        .. literalinclude:: ../../examples/szdiagnostic/szdiagnostic_constructor.py
            :linenos:
            :language: python
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        instance_name: str = "",
        settings: Union[str, Dict[Any, Any]] = "",
        config_id: int = 0,
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """

        self.initialized = False
        self.instance_name = instance_name
        self.settings = settings
        self.config_id = config_id
        self.verbose_logging = verbose_logging

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
        # Must be synchronized with g2/sdk/c/libg2diagnostic.h

        self.library_handle.SzDiagnostic_checkDatastorePerformance_helper.argtypes = [
            c_longlong
        ]
        self.library_handle.SzDiagnostic_checkDatastorePerformance_helper.restype = (
            SzDiagnosticCheckDatastorePerformanceResult
        )
        self.library_handle.SzDiagnostic_destroy.argtypes = []
        self.library_handle.SzDiagnostic_destroy.restype = c_longlong
        self.library_handle.SzDiagnostic_getDatastoreInfo_helper.argtypes = []
        self.library_handle.SzDiagnostic_getDatastoreInfo_helper.restype = (
            SzDiagnosticGetDatastoreInfoResult
        )
        self.library_handle.SzDiagnostic_getFeature_helper.argtypes = [c_longlong]
        self.library_handle.SzDiagnostic_getFeature_helper.restype = (
            SzDiagnosticGetFeatureResult
        )
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
        # TODO - Ant -
        # self.library_handle.SzHelper_free.argtypes = [c_char_p]
        self.library_handle.G2GoHelper_free.argtypes = [c_char_p]

        if not self.instance_name or len(self.settings) == 0:
            raise sdk_exception(2)

        # Initialize Senzing engine.
        self._initialize(
            instance_name=self.instance_name,
            settings=self.settings,
            config_id=self.config_id,
            verbose_logging=self.verbose_logging,
        )
        self.initialized = True

    def __del__(self) -> None:
        """Destructor"""
        if self.initialized:
            with suppress(Exception):
                self._destroy()

    # -------------------------------------------------------------------------
    # SzDiagnostic methods
    # -------------------------------------------------------------------------

    def check_datastore_performance(self, seconds_to_run: int, **kwargs: Any) -> str:
        result = self.library_handle.SzDiagnostic_checkDatastorePerformance_helper(
            seconds_to_run
        )
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    def _destroy(self, **kwargs: Any) -> None:
        _ = self.library_handle.SzDiagnostic_destroy()

    def get_datastore_info(self, **kwargs: Any) -> str:
        result = self.library_handle.SzDiagnostic_getDatastoreInfo_helper()
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    # NOTE This is included but not to be documented
    # NOTE Is used by sz_explorer
    def get_feature(self, feature_id: int, **kwargs: Any) -> str:
        result = self.library_handle.SzDiagnostic_getFeature_helper(feature_id)
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    @catch_exceptions
    def _initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        config_id: int = 0,
        verbose_logging: int = 0,
        **kwargs: Any,
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

    def purge_repository(self, **kwargs: Any) -> None:
        result = self.library_handle.SzDiagnostic_purgeRepository()
        self.check_result(result)

    def reinitialize(self, config_id: int, **kwargs: Any) -> None:
        result = self.library_handle.SzDiagnostic_reinit(config_id)
        self.check_result(result)
