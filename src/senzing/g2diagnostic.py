"""
The `g2diagnostic` package is used to inspect the Senzing environment.
It is a wrapper over Senzing's G2Diagnostic C binding.
It conforms to the interface specified in
`g2diagnostic_abstract.py <https://github.com/senzing-garage/g2-sdk-python-next/blob/main/src/senzing/g2diagnostic_abstract.py>`_

To use g2diagnostic,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/g2/lib
"""

# pylint: disable=R0903,R0915

import os
from ctypes import (
    POINTER,
    Structure,
    c_char,
    c_char_p,
    c_int,
    c_longlong,
    c_size_t,
    cast,
    cdll,
)
from typing import Any, Dict, Union

from .g2diagnostic_abstract import G2DiagnosticAbstract
from .g2exception import G2Exception, new_g2exception
from .g2helpers import (
    as_c_char_p,
    as_c_int,
    as_str,
    cast_ctypes_exceptions,
    find_file_in_path,
)
from .g2version import is_supported_senzingapi_version

# Metadata

__all__ = ["G2Diagnostic"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-27"

SENZING_PRODUCT_ID = "5042"  # See https://github.com/senzing-garage/knowledge-base/blob/main/lists/senzing-component-ids.md
CALLER_SKIP = 6

# -----------------------------------------------------------------------------
# Classes that are result structures from calls to Senzing
# -----------------------------------------------------------------------------


class G2ResponseReturnCodeResult(Structure):
    """Simple response, return_code structure"""

    _fields_ = [
        ("response", POINTER(c_char)),
        ("return_code", c_longlong),
    ]


class G2DiagnosticCheckDBPerfResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2Diagnostic_checkDBPerf_result"""


class G2DiagnosticGetDBInfoResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2Diagnostic_getDBInfo_result"""


# -----------------------------------------------------------------------------
# G2Diagnostic class
# -----------------------------------------------------------------------------


class G2Diagnostic(G2DiagnosticAbstract):
    """
    The `init` method initializes the Senzing G2Diagnostic object.
    It must be called prior to any other calls.

    **Note:** If the G2Diagnostic constructor is called with parameters,
    the constructor will automatically call the `init()` method.

    Example:

    .. code-block:: python

        g2_diagnostic = g2diagnostic.G2Diagnostic(module_name, ini_params)


    If the G2Diagnostic constructor is called without parameters,
    the `init()` method must be called to initialize the use of G2Product.

    Example:

    .. code-block:: python

        g2_diagnostic = g2diagnostic.G2Diagnostic()
        g2_diagnostic.init(module_name, ini_params)

    Either `module_name` and `ini_params` must both be specified or neither must be specified.
    Just specifying one or the other results in a **G2Exception**.

    Parameters:
        module_name:
            `Optional:` A name for the auditing node, to help identify it within system logs. Default: ""
        ini_params:
            `Optional:` A JSON string containing configuration parameters. Default: ""
        init_config_id:
            `Optional:` Specify the ID of a specific Senzing configuration. Default: 0 - Use default Senzing configuration
        verbose_logging:
            `Optional:` A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging. Default: 0

    Raises:
        TypeError: Incorrect datatype detected on input parameter.
        g2exception.G2Exception: Failed to load the G2 library or incorrect `module_name`, `ini_params` combination.


    .. collapse:: Example:

        .. literalinclude:: ../../examples/g2diagnostic/g2diagnostic_constructor.py
            :linenos:
            :language: python
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        module_name: str = "",
        ini_params: Union[str, Dict[Any, Any]] = "",
        init_config_id: int = 0,
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
        self.ini_params = as_str(ini_params)
        self.init_config_id = init_config_id
        self.module_name = module_name
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
            raise G2Exception("Failed to load the G2 library") from err

        # Initialize C function input parameters and results.
        # Must be synchronized with g2/sdk/c/libg2diagnostic.h

        # self.library_handle.G2Diagnostic_checkDBPerf.argtypes = [c_int, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Diagnostic_checkDBPerf.restype = c_longlong
        self.library_handle.G2Diagnostic_checkDBPerf_helper.argtypes = [c_longlong]
        self.library_handle.G2Diagnostic_checkDBPerf_helper.restype = (
            G2DiagnosticCheckDBPerfResult
        )
        self.library_handle.G2Diagnostic_clearLastException.argtypes = []
        self.library_handle.G2Diagnostic_clearLastException.restype = None
        # self.library_handle.G2Diagnostic_closeEntityListBySize.argtypes = [c_void_p]
        # self.library_handle.G2Diagnostic_closeEntityListBySize.restype = c_longlong
        self.library_handle.G2Diagnostic_destroy.argtypes = []
        self.library_handle.G2Diagnostic_destroy.restype = c_longlong
        # self.library_handle.G2Diagnostic_fetchNextEntityBySize.argtypes = [c_void_p, c_char_p, c_size_t]
        # self.library_handle.G2Diagnostic_fetchNextEntityBySize.restype = c_longlong
        # self.library_handle.G2Diagnostic_findEntitiesByFeatureIDs.argtypes = [c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Diagnostic_findEntitiesByFeatureIDs.restype = c_longlong
        self.library_handle.G2Diagnostic_getAvailableMemory.argtypes = []
        self.library_handle.G2Diagnostic_getAvailableMemory.restype = c_longlong
        # self.library_handle.G2Diagnostic_getDataSourceCounts.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Diagnostic_getDataSourceCounts.restype = c_longlong
        # self.library_handle.G2Diagnostic_getDBInfo.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Diagnostic_getDBInfo.restype = c_longlong
        self.library_handle.G2Diagnostic_getDBInfo_helper.argtypes = []
        self.library_handle.G2Diagnostic_getDBInfo_helper.restype = (
            G2DiagnosticGetDBInfoResult
        )
        # self.library_handle.G2Diagnostic_getEntityDetails.argtypes = [c_longlong, c_int, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Diagnostic_getEntityDetails.restype = c_longlong
        # self.library_handle.G2Diagnostic_getEntityListBySize.argtypes = [c_ulonglong, POINTER(c_void_p)]
        # self.library_handle.G2Diagnostic_getEntityListBySize.restype = c_longlong
        # self.library_handle.G2Diagnostic_getEntityResume.argtypes = [c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Diagnostic_getEntityResume.restype = c_longlong
        # self.library_handle.G2Diagnostic_getEntitySizeBreakdown.argtypes = [c_size_t, c_int, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Diagnostic_getEntitySizeBreakdown.restype = c_longlong
        # self.library_handle.G2Diagnostic_getFeature.argtypes = [c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Diagnostic_getFeature.restype = c_longlong
        # self.library_handle.G2Diagnostic_getGenericFeatures.argtypes = [c_char_p, c_size_t, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Diagnostic_getGenericFeatures.restype = c_longlong
        self.library_handle.G2Diagnostic_getLastException.argtypes = [
            POINTER(c_char),
            c_size_t,
        ]
        self.library_handle.G2Diagnostic_getLastException.restype = c_longlong
        self.library_handle.G2Diagnostic_getLastExceptionCode.argtypes = []
        self.library_handle.G2Diagnostic_getLastExceptionCode.restype = c_longlong
        self.library_handle.G2Diagnostic_getLogicalCores.argtypes = []
        self.library_handle.G2Diagnostic_getLogicalCores.restype = c_longlong
        # self.library_handle.G2Diagnostic_getMappingStatistics.argtypes = [ c_int, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Diagnostic_getMappingStatistics.restype = c_longlong
        self.library_handle.G2Diagnostic_getPhysicalCores.argtypes = []
        self.library_handle.G2Diagnostic_getPhysicalCores.restype = c_longlong
        # self.library_handle.G2Diagnostic_getRelationshipDetails.argtypes = [c_longlong, c_int, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Diagnostic_getRelationshipDetails.restype = c_longlong
        # self.library_handle.G2Diagnostic_getResolutionStatistics.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Diagnostic_getResolutionStatistics.restype = c_longlong
        self.library_handle.G2Diagnostic_getTotalSystemMemory.argtypes = []
        self.library_handle.G2Diagnostic_getTotalSystemMemory.restype = c_longlong
        self.library_handle.G2Diagnostic_init.argtypes = [c_char_p, c_char_p, c_int]
        self.library_handle.G2Diagnostic_init.restype = c_longlong
        self.library_handle.G2Diagnostic_initWithConfigID.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
            c_int,
        ]
        self.library_handle.G2Diagnostic_initWithConfigID.restype = c_longlong
        self.library_handle.G2Diagnostic_reinit.argtypes = [c_longlong]
        self.library_handle.G2Diagnostic_reinit.restype = c_longlong
        self.library_handle.G2GoHelper_free.argtypes = [c_char_p]

        # Initialize Senzing engine.

        if (len(self.module_name) == 0) or (len(self.ini_params) == 0):
            if len(self.module_name) + len(self.ini_params) != 0:
                raise self.new_exception(4021, self.module_name, self.ini_params)
        if len(self.module_name) > 0:
            self.auto_init = True
            self.init(self.module_name, self.ini_params, self.verbose_logging)

    def __del__(self) -> None:
        """Destructor"""
        if self.auto_init:
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

    @cast_ctypes_exceptions
    def check_db_perf(self, seconds_to_run: int, *args: Any, **kwargs: Any) -> str:
        result = self.library_handle.G2Diagnostic_checkDBPerf_helper(seconds_to_run)
        try:
            if result.return_code != 0:
                raise self.new_exception(4001, result.return_code)
            result_response = cast(result.response, c_char_p).value
            result_response_str = result_response.decode() if result_response else ""
        finally:
            self.library_handle.G2GoHelper_free(result.response)
        return result_response_str

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        result = self.library_handle.G2Diagnostic_destroy()
        if result != 0:
            raise self.new_exception(4003, result)

    # TODO: Likely going away in V4
    def get_available_memory(self, *args: Any, **kwargs: Any) -> int:
        result = self.library_handle.G2Diagnostic_getAvailableMemory()
        return int(result)

    def get_db_info(self, *args: Any, **kwargs: Any) -> str:
        result = self.library_handle.G2Diagnostic_getDBInfo_helper()
        try:
            if result.return_code != 0:
                raise self.new_exception(4007, result.return_code)
            result_response = cast(result.response, c_char_p).value
            result_response_str = result_response.decode() if result_response else ""
        finally:
            self.library_handle.G2GoHelper_free(result.response)
        return result_response_str

    # TODO: Likely going away in V4
    def get_logical_cores(self, *args: Any, **kwargs: Any) -> int:
        return int(self.library_handle.G2Diagnostic_getLogicalCores())

    # TODO: Likely going away in V4
    # BUG: Returns wrong value!
    def get_physical_cores(self, *args: Any, **kwargs: Any) -> int:
        return int(self.library_handle.G2Diagnostic_getPhysicalCores())

    # TODO: Likely going away in V4
    def get_total_system_memory(self, *args: Any, **kwargs: Any) -> int:
        result = self.library_handle.G2Diagnostic_getTotalSystemMemory()
        return int(result)

    def init(
        self,
        module_name: str,
        ini_params: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        result = self.library_handle.G2Diagnostic_init(
            as_c_char_p(module_name),
            as_c_char_p(as_str(ini_params)),
            as_c_int(verbose_logging),
        )
        if result < 0:
            raise self.new_exception(
                4018, module_name, as_str(ini_params), verbose_logging, result
            )

    def init_with_config_id(
        self,
        module_name: str,
        ini_params: Union[str, Dict[Any, Any]],
        init_config_id: int,
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        result = self.library_handle.G2Diagnostic_initWithConfigID(
            as_c_char_p(module_name),
            as_c_char_p(as_str(ini_params)),
            as_c_int(init_config_id),
            as_c_int(verbose_logging),
        )
        if result < 0:
            raise self.new_exception(
                4019,
                module_name,
                as_str(ini_params),
                init_config_id,
                verbose_logging,
                result,
            )

    @cast_ctypes_exceptions
    def reinit(self, init_config_id: int, *args: Any, **kwargs: Any) -> None:
        result = self.library_handle.G2Diagnostic_reinit(init_config_id)
        if result < 0:
            raise self.new_exception(4020, init_config_id, result)
