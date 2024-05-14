"""
The `szdiagnostic` package is used to inspect the Senzing environment.
It is a wrapper over Senzing's G2Diagnostic C binding.
It conforms to the interface specified in
`szdiagnostic_abstract.py <https://github.com/senzing-garage/sz-sdk-python/blob/main/src/senzing_abstract/szdiagnostic_abstract.py>`_

To use szdiagnostic,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/g2/lib
"""

# pylint: disable=R0903

import os
from ctypes import POINTER, Structure, c_char, c_char_p, c_int, c_longlong, cdll
from types import TracebackType
from typing import Any, Dict, Optional, Type, Union

from senzing import (
    FreeCResources,
    SzDiagnosticAbstract,
    SzError,
    as_c_char_p,
    as_python_str,
    as_str,
    catch_ctypes_exceptions,
    find_file_in_path,
    new_szexception,
)

from .szversion import is_supported_senzingapi_version

# Metadata

__all__ = ["SzDiagnostic"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-27"

SENZING_PRODUCT_ID = "5042"  # See https://github.com/senzing-garage/knowledge-base/blob/main/lists/senzing-component-ids.md

# -----------------------------------------------------------------------------
# Classes that are result structures from calls to Senzing
# -----------------------------------------------------------------------------


class G2ResponseReturnCodeResult(Structure):
    """Simple response, return_code structure"""

    _fields_ = [
        ("response", POINTER(c_char)),
        ("return_code", c_longlong),
    ]


class G2DiagnosticCheckDatastorePerformanceResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2Diagnostic_checkDatastorePerformance_result"""


class G2DiagnosticGetDatastoreInfoResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2Diagnostic_getDatastoreInfo_result"""


class G2DiagnosticGetFeatureResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2Diagnostic_getFeature_result"""


# -----------------------------------------------------------------------------
# SzDiagnostic class
# -----------------------------------------------------------------------------


class SzDiagnostic(SzDiagnosticAbstract):
    """
    The `initialize` method initializes the Senzing SzDiagnostic object.
    It must be called prior to any other calls.

    **Note:** If the SzDiagnostic constructor is called with parameters,
    the constructor will automatically call the `initialize()` method.

    Example:

    .. code-block:: python

        sz_diagnostic = SzDiagnostic(instance_name, settings)


    If the SzDiagnostic constructor is called without parameters,
    the `inititialize()` method must be called to initialize the use of G2Product.

    Example:

    .. code-block:: python

        sz_diagnostic = SzDiagnostic()
        sz_diagnostic.inititialize(instance_name, settings)

    Either `instance_name` and `settings` must both be specified or neither must be specified.
    Just specifying one or the other results in a **G2Exception**.

    Parameters:
        instance_name:
            `Optional:` A name for the auditing node, to help identify it within system logs. Default: ""
        settings:
            `Optional:` A JSON string containing configuration parameters. Default: ""
        config_id:
            `Optional:` Specify the ID of a specific Senzing configuration. Default: 0 - Use default Senzing configuration
        verbose_logging:
            `Optional:` A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging. Default: 0

    Raises:
        TypeError: Incorrect datatype detected on input parameter.
        SzError: Failed to load the G2 library or incorrect `instance_name`, `settings` combination.


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
        # pylint: disable=W0613

        # Verify parameters.

        self.auto_init = False
        self.settings = as_str(settings)
        self.config_id = config_id
        self.instance_name = instance_name
        self.verbose_logging = verbose_logging

        # Determine if Senzing API version is acceptable.

        is_supported_senzingapi_version()

        # Load binary library.

        try:
            if os.name == "nt":
                # TODO: See if find_file_in_path can be factored out.
                self.library_handle = cdll.LoadLibrary(find_file_in_path("G2.dll"))
            else:
                self.library_handle = cdll.LoadLibrary("libG2.so")
        except OSError as err:
            # TODO: Change to Sz library when the libG2.so is changed in a build
            raise SzError("Failed to load the G2 library") from err

        # Initialize C function input parameters and results.
        # Must be synchronized with g2/sdk/c/libg2diagnostic.h

        self.library_handle.G2Diagnostic_checkDatastorePerformance_helper.argtypes = [
            c_longlong
        ]
        self.library_handle.G2Diagnostic_checkDatastorePerformance_helper.restype = (
            G2DiagnosticCheckDatastorePerformanceResult
        )
        self.library_handle.G2Diagnostic_destroy.argtypes = []
        self.library_handle.G2Diagnostic_destroy.restype = c_longlong
        self.library_handle.G2Diagnostic_getDatastoreInfo_helper.argtypes = []
        self.library_handle.G2Diagnostic_getDatastoreInfo_helper.restype = (
            G2DiagnosticGetDatastoreInfoResult
        )
        self.library_handle.G2Diagnostic_getFeature_helper.argtypes = [c_longlong]
        self.library_handle.G2Diagnostic_getFeature_helper.restype = (
            G2DiagnosticGetFeatureResult
        )
        self.library_handle.G2Diagnostic_init.argtypes = [c_char_p, c_char_p, c_int]
        self.library_handle.G2Diagnostic_init.restype = c_longlong
        self.library_handle.G2Diagnostic_initWithConfigID.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2Diagnostic_initWithConfigID.restype = c_longlong
        self.library_handle.G2Diagnostic_reinit.argtypes = [c_longlong]
        self.library_handle.G2Diagnostic_reinit.restype = c_longlong
        self.library_handle.G2GoHelper_free.argtypes = [c_char_p]

        # Initialize Senzing engine.

        if (len(self.instance_name) == 0) or (len(self.settings) == 0):
            if len(self.instance_name) + len(self.settings) != 0:
                raise self.new_exception(4007, self.instance_name, self.settings)
        if len(self.instance_name) > 0:
            self.auto_init = True
            self.initialize(
                instance_name=self.instance_name,
                settings=self.settings,
                config_id=self.config_id,
                verbose_logging=self.verbose_logging,
            )

    def __del__(self) -> None:
        """Destructor"""
        if self.auto_init:
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
    # Exception helpers
    # -------------------------------------------------------------------------

    def new_exception(self, error_id: int, *args: Any) -> Exception:
        """
        Generate a new exception based on the error_id.

        :meta private:
        """
        return new_szexception(
            self.library_handle.G2Diagnostic_getLastException,
            self.library_handle.G2Diagnostic_clearLastException,
            SENZING_PRODUCT_ID,
            error_id,
            self.ID_MESSAGES,
            *args,
        )

    # -------------------------------------------------------------------------
    # SzDiagnostic methods
    # -------------------------------------------------------------------------

    def check_datastore_performance(self, seconds_to_run: int, **kwargs: Any) -> str:
        result = self.library_handle.G2Diagnostic_checkDatastorePerformance_helper(
            seconds_to_run
        )
        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4001,
                    seconds_to_run,
                    result.return_code,
                )
            return as_python_str(result.response)

    def destroy(self, **kwargs: Any) -> None:
        result = self.library_handle.G2Diagnostic_destroy()
        if result != 0:
            raise self.new_exception(4002, result)

    def get_datastore_info(self, **kwargs: Any) -> str:
        result = self.library_handle.G2Diagnostic_getDatastoreInfo_helper()
        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4003,
                    result.return_code,
                )
            return as_python_str(result.response)

    # NOTE This is included but not to be documented
    def get_feature(self, feature_id: int, **kwargs: Any) -> str:
        result = self.library_handle.G2Diagnostic_getFeature_helper(feature_id)
        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4003,
                    feature_id,
                    result.return_code,
                )
            return as_python_str(result.response)

    @catch_ctypes_exceptions
    def initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        config_id: Optional[int] = 0,
        verbose_logging: Optional[int] = 0,
        **kwargs: Any,
    ) -> None:
        if config_id == 0:
            result = self.library_handle.G2Diagnostic_init(
                as_c_char_p(instance_name),
                as_c_char_p(as_str(settings)),
                verbose_logging,
            )
            if result < 0:
                raise self.new_exception(
                    4004,
                    instance_name,
                    as_str(settings),
                    verbose_logging,
                    config_id,
                    result,
                )
            return
        result = self.library_handle.G2Diagnostic_initWithConfigID(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            config_id,
            verbose_logging,
        )
        if result < 0:
            raise self.new_exception(
                4003,
                instance_name,
                settings,
                verbose_logging,
                config_id,
                result,
            )

    def purge_repository(self, **kwargs: Any) -> None:
        result = self.library_handle.G2Diagnostic_purgeRepository()
        if result < 0:
            raise self.new_exception(4005, result)

    def reinitialize(self, config_id: int, **kwargs: Any) -> None:
        result = self.library_handle.G2Diagnostic_reinit(config_id)
        if result < 0:
            raise self.new_exception(4006, config_id, result)
