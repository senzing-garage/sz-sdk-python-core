"""
The g2engine package is used to insert, update, delete and query records and entities in the Senzing product.
It is a wrapper over Senzing's G2Engine C binding.
It conforms to the interface specified in
`g2engine_abstract.py <https://github.com/Senzing/g2-sdk-python-next/blob/main/src/senzing/g2engine_abstract.py>`_

To use g2engine,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/g2/lib
"""

import ctypes
import os
from typing import Any, Tuple

from .g2engine_abstract import G2EngineAbstract
from .g2exception import G2Exception, new_g2exception
from .g2helpers import find_file_in_path

# Metadata

__all__ = ["G2Engine"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-01"

SENZING_PRODUCT_ID = "5043"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md
CALLER_SKIP = 6  # Number of stack frames to skip when reporting location in Exception.

# -----------------------------------------------------------------------------
# Classes that are result structures from calls to Senzing
# -----------------------------------------------------------------------------


class G2AddRecordWithInfoRresult(ctypes.Structure):
    """In golang_helpers.h G2_addRecordWithInfo_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]


class G2DeleteRecordWithInfoResult(ctypes.Structure):
    """In golang_helpers.h G2_deleteRecordWithInfo_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2ExportConfigAndConfigIDResult(ctypes.Structure):
    """In golang_helpers.h G2_exportConfigAndConfigID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("config_id", ctypes.c_longlong),
        ("config", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2ExportConfigResult(ctypes.Structure):
    """In golang_helpers.h G2_exportConfig_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2ExportCSVEntityReportResult(ctypes.Structure):
    """In golang_helpers.h G2_exportCSVEntityReport_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("export_handle", ctypes.c_void_p),
        ("return_code", ctypes.c_longlong),
    ]

class G2ExportJSONEntityReportResult(ctypes.Structure):
    """In golang_helpers.h G2_exportJSONEntityReport_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("export_handle", ctypes.c_void_p),
        ("return_code", ctypes.c_longlong),
    ]

class G2FetchNextResult(ctypes.Structure):
    """In golang_helpers.h G2_fetchNext_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindInterestingEntitiesByEntityIDResult(ctypes.Structure):
    """In golang_helpers.h G2_findInterestingEntitiesByEntityID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindInterestingEntitiesByRecordIDResult(ctypes.Structure):
    """In golang_helpers.h G2_findInterestingEntitiesByRecordID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindNetworkByEntityIDResult(ctypes.Structure):
    """In golang_helpers.h G2_findNetworkByEntityID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindNetworkByEntityID_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_findNetworkByEntityID_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindNetworkByRecordIDResult(ctypes.Structure):
    """In golang_helpers.h G2_findNetworkByRecordID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindNetworkByRecordID_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_findNetworkByRecordID_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindPathByEntityIDResult(ctypes.Structure):
    """In golang_helpers.h G2_findPathByEntityID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindPathByEntityID_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_findPathByEntityID_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindPathByRecordIDResult(ctypes.Structure):
    """In golang_helpers.h G2_findPathByRecordID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindPathByRecordID_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_findPathByRecordID_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindPathExcludingByEntityIDResult(ctypes.Structure):
    """In golang_helpers.h G2_findPathExcludingByEntityID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindPathExcludingByEntityID_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_findPathExcludingByEntityID_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindPathExcludingByRecordIDResult(ctypes.Structure):
    """In golang_helpers.h G2_findPathExcludingByRecordID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindPathExcludingByRecordID_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_findPathExcludingByRecordID_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindPathIncludingSourceByEntityIDResult(ctypes.Structure):
    """In golang_helpers.h G2_findPathIncludingSourceByEntityID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindPathIncludingSourceByEntityID_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_findPathIncludingSourceByEntityID_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindPathIncludingSourceByRecordIDResult(ctypes.Structure):
    """In golang_helpers.h G2_findPathIncludingSourceByRecordID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2FindPathIncludingSourceByRecordID_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_findPathIncludingSourceByRecordID_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2GetActiveConfigIDResult(ctypes.Structure):
    """In golang_helpers.h G2_getActiveConfigID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("config_id", ctypes.c_longlong),
        ("return_code", ctypes.c_longlong),
    ]

class G2GetEntityByEntityIDResult(ctypes.Structure):
    """In golang_helpers.h G2_getEntityByEntityID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2GetEntityByEntityID_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_getEntityByEntityID_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2GetEntityByRecordIDResult(ctypes.Structure):
    """In golang_helpers.h G2_getEntityByRecordID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2GetEntityByRecordID_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_getEntityByRecordID_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2GetRecordResult(ctypes.Structure):
    """In golang_helpers.h G2_getRecord_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2GetRecord_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_getRecord_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2GetRedoRecordResult(ctypes.Structure):
    """In golang_helpers.h G2_getRedoRecord_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2GetRepositoryLastModifiedTimeResult(ctypes.Structure):
    """In golang_helpers.h G2_getRepositoryLastModifiedTime_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("time", ctypes.c_longlong),
        ("return_code", ctypes.c_longlong),
    ]

class G2GetVirtualEntityByRecordIDResult(ctypes.Structure):
    """In golang_helpers.h G2_getVirtualEntityByRecordID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2GetVirtualEntityByRecordID_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_getVirtualEntityByRecordID_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2HowEntityByEntityIDResult(ctypes.Structure):
    """In golang_helpers.h G2_howEntityByEntityID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2HowEntityByEntityID_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_howEntityByEntityID_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2ProcessWithInfoResult(ctypes.Structure):
    """In golang_helpers.h G2_processWithInfo_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2ReevaluateEntityWithInfoResult(ctypes.Structure):
    """In golang_helpers.h G2_reevaluateEntityWithInfo_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2ReevaluateRecordWithInfoResult(ctypes.Structure):
    """In golang_helpers.h G2_reevaluateRecordWithInfo_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2ReplaceRecordWithInfoResult(ctypes.Structure):
    """In golang_helpers.h G2_replaceRecordWithInfo_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2SearchByAttributesResult(ctypes.Structure):
    """In golang_helpers.h G2_searchByAttributes_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2SearchByAttributes_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_searchByAttributes_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2StatsResult(ctypes.Structure):
    """In golang_helpers.h G2_stats_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2WhyEntitiesResult(ctypes.Structure):
    """In golang_helpers.h G2_whyEntities_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2WhyEntities_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_whyEntities_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2WhyEntityByEntityIDResult(ctypes.Structure):
    """In golang_helpers.h G2_whyEntityByEntityID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2WhyEntityByEntityID_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_whyEntityByEntityID_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2WhyEntityByRecordIDResult(ctypes.Structure):
    """In golang_helpers.h G2_whyEntityByRecordID_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2WhyEntityByRecordID_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_whyEntityByRecordID_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2WhyRecordsResult(ctypes.Structure):
    """In golang_helpers.h G2_whyRecords_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]

class G2WhyRecords_V2Result(ctypes.Structure):
    """In golang_helpers.h G2_whyRecords_V2_result"""
    # pylint: disable=R0903
    _fields_ = [
        ("response", ctypes.POINTER(ctypes.c_char)),
        ("return_code", ctypes.c_longlong),
    ]


# -----------------------------------------------------------------------------
# G2Engine class
# -----------------------------------------------------------------------------


class G2Engine(G2EngineAbstract):
    """
    The `init` method initializes the Senzing G2Engine object.
    It must be called prior to any other calls.

    **Note:** If the G2Engine constructor is called with parameters,
    the constructor will automatically call the `init()` method.

    Example:

    .. code-block:: python

        g2_engine = g2engine.G2Engine(ENGINE_MODULE_NAME, ENGINE_CONFIGURATION_JSON)


    If the G2Engine constructor is called without parameters,
    the `init()` method must be called to initialize the use of G2Engine.

    Example:

    .. code-block:: python

        g2_engine = g2engine.G2Engine()
        g2_engine.init(ENGINE_MODULE_NAME, ENGINE_CONFIGURATION_JSON, ENGINE_VERBOSE_LOGGING)

    Either `module_name` and `ini_params` must both be specified or neither must be specified.
    Just specifying one or the other results in a **G2Exception**.

    Parameters:
        module_name:
            `Optional:` A name for the auditing node, to help identify it within system logs. Default: ""
        ini_params:
            `Optional:` A JSON string containing configuration parameters. Default: ""
        init_config_id:
            `Optional:` Specify the ID of a specific Senzing configuration. Default: 0 - Use current Senzing configuration
        verbose_logging:
            `Optional:` A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging. Default: 0

    Raises:
        G2Exception: Raised when input parameters are incorrect.

    .. collapse:: Example:

        .. literalinclude:: ../../examples/g2engine_constructor.py
            :linenos:
            :language: python
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        *args: Any,
        module_name: str = "",
        ini_params: str = "",
        init_config_id: int = 0,
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """

        # Verify parameters.

        if (len(module_name) == 0) or (len(ini_params) == 0):
            if len(module_name) + len(ini_params) != 0:
                raise self.new_exception(9999, module_name, ini_params)

        self.ini_params = ini_params
        self.module_name = module_name
        self.init_config_id = init_config_id
        self.verbose_logging = verbose_logging

        # Load binary library.

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
        # Must be synchronized with g2/sdk/c/libg2engine.h


        self.library_handle.G2_addRecord.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p]
        self.library_handle.G2_addRecord.restype = c_int
        self.library_handle.G2_addRecordWithInfo.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_addRecordWithInfoWithReturnedRecordID.argtypes = [c_char_p, c_char_p, c_char_p, c_longlong, c_char_p, c_size_t, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def3]
        self.library_handle.G2_addRecordWithInfoWithReturnedRecordID.restype = c_int
        self.library_handle.G2_addRecordWithReturnedRecordID.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_size_t]
        self.library_handle.G2_checkRecord.argtypes = [c_char_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_clearLastException.argtypes = []
        self.library_handle.G2_clearLastException.restype = None
        self.library_handle.G2_closeExport.argtypes = [c_void_p]
        self.library_handle.G2_closeExport.restype = c_int
        self.library_handle.G2_deleteRecordWithInfo.argtypes = [c_char_p, c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_exportConfig.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_exportCSVEntityReport.argtypes = [c_char_p, c_longlong, POINTER(c_void_p)]
        self.library_handle.G2_exportCSVEntityReport.restype = c_int
        self.library_handle.G2_exportJSONEntityReport.argtypes = [c_longlong, POINTER(c_void_p)]
        self.library_handle.G2_exportJSONEntityReport.restype = c_int
        self.library_handle.G2_fetchNext.argtypes = [c_void_p, c_char_p, c_size_t]
        self.library_handle.G2_fetchNext.restype = c_int
        self.library_handle.G2_findInterestingEntitiesByEntityID.argtypes = [c_longlong, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_findInterestingEntitiesByEntityID.restype = c_int
        self.library_handle.G2_findInterestingEntitiesByRecordID.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_findInterestingEntitiesByRecordID.restype = c_int
        self.library_handle.G2_findNetworkByEntityID_V2.argtypes = [c_char_p, c_int, c_int, c_int, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_findNetworkByEntityID_V2.restype = c_int
        self.library_handle.G2_findNetworkByRecordID_V2.argtypes = [c_char_p, c_int, c_int, c_int, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_findNetworkByRecordID_V2.restype = c_int
        self.library_handle.G2_findPathByEntityID_V2.argtypes = [c_longlong, c_longlong, c_int, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_findPathByEntityID_V2.restype = c_int
        self.library_handle.G2_findPathByRecordID_V2.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_findPathByRecordID_V2.restype = c_int
        self.library_handle.G2_findPathExcludingByEntityID_V2.argtypes = [c_longlong, c_longlong, c_int, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_findPathExcludingByEntityID_V2.restype = c_int
        self.library_handle.G2_findPathExcludingByRecordID_V2.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_findPathExcludingByRecordID_V2.restype = c_int
        self.library_handle.G2_findPathIncludingSourceByEntityID_V2.argtypes = [c_longlong, c_longlong, c_int, c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_findPathIncludingSourceByEntityID_V2.restype = c_int
        self.library_handle.G2_findPathIncludingSourceByRecordID_V2.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_findPathIncludingSourceByRecordID_V2.restype = c_int
        self.library_handle.G2_getActiveConfigID.argtypes = [POINTER(c_longlong)]
        self.library_handle.G2_getEntityByEntityID_V2.argtypes = [c_longlong, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_getEntityByEntityID_V2.restype = c_int
        self.library_handle.G2_getEntityByRecordID_V2.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_getEntityByRecordID_V2.restype = c_int
        self.library_handle.G2_getLastException.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_size_t,]
        self.library_handle.G2_getLastException.restype = ctypes.c_longlong
        self.library_handle.G2_getLastExceptionCode.argtypes = []
        self.library_handle.G2_getLastExceptionCode.restype = c_int
        self.library_handle.G2_getRecord_V2.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_getRecord_V2.restype = c_int
        self.library_handle.G2_getRedoRecord.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_getRedoRecord.restype = c_int
        self.library_handle.G2_getRepositoryLastModifiedTime.argtypes = [POINTER(c_longlong)]
        self.library_handle.G2_getVirtualEntityByRecordID_V2.argtypes = [c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_getVirtualEntityByRecordID_V2.restype = c_int
        self.library_handle.G2_howEntityByEntityID_V2.argtypes = [c_longlong, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_howEntityByEntityID_V2.restype = c_int
        self.library_handle.G2_init.argtypes = [c_char_p, c_char_p, c_int]
        self.library_handle.G2_initWithConfigID.argtypes = [c_char_p, c_char_p, c_longlong, c_int]
        self.library_handle.G2_process.argtypes = [c_char_p]
        self.library_handle.G2_process.restype = c_int
        self.library_handle.G2_processRedoRecord.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_processRedoRecord.restype = c_int
        self.library_handle.G2_processWithInfo.argtypes = [c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_processWithResponseResize.argtypes = [c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_reevaluateEntity.argtypes = [c_longlong, c_longlong]
        self.library_handle.G2_reevaluateEntityWithInfo.argtypes = [c_int, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_reevaluateRecord.argtypes = [c_char_p, c_char_p, c_longlong]
        self.library_handle.G2_reevaluateRecord.restype = c_int
        self.library_handle.G2_reevaluateRecordWithInfo.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_reinit.argtypes = [c_longlong]
        self.library_handle.G2_replaceRecordWithInfo.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_searchByAttributes_V2.argtypes = [c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_searchByAttributes_V3.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_stats.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_whyEntities_V2.argtypes = [c_longlong, c_longlong, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_whyEntities_V2.restype = c_int
        self.library_handle.G2_whyEntityByEntityID_V2.argtypes = [c_longlong, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_whyEntityByEntityID_V2.restype = c_int
        self.library_handle.G2_whyEntityByRecordID_V2.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_whyEntityByRecordID_V2.restype = c_int
        self.library_handle.G2_whyRecordInEntity_V2.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_whyRecordInEntity_V2.restype = c_int
        self.library_handle.G2_whyRecords_V2.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_whyRecords_V2.restype = c_int
        self.library_handle.G2GoHelper_free.argtypes = [ctypes.c_char_p]


#
# _DLEXPORT struct G2_addRecordWithInfo_result G2_addRecordWithInfo_helper(const char *dataSourceCode, const char *recordID, const char *jsonData, const char *loadID, const long long flags);
# _DLEXPORT long long G2_closeExport_helper(uintptr_t responseHandle);
# _DLEXPORT struct G2_deleteRecordWithInfo_result G2_deleteRecordWithInfo_helper(const char *dataSourceCode, const char *recordID, const char *loadID, const long long flags);
# _DLEXPORT struct G2_exportConfigAndConfigID_result G2_exportConfigAndConfigID_helper();
# _DLEXPORT struct G2_exportConfig_result G2_exportConfig_helper();
# _DLEXPORT struct G2_exportCSVEntityReport_result G2_exportCSVEntityReport_helper(const char *csvColumnList, const long long flags);
# _DLEXPORT struct G2_exportJSONEntityReport_result G2_exportJSONEntityReport_helper(const long long flags);
# _DLEXPORT struct G2_findInterestingEntitiesByEntityID_result G2_findInterestingEntitiesByEntityID_helper(long long entityID, long long flags);
# _DLEXPORT struct G2_findInterestingEntitiesByRecordID_result G2_findInterestingEntitiesByRecordID_helper(const char *dataSourceCode, const char *recordID, long long flags);
# _DLEXPORT struct G2_findNetworkByEntityID_result G2_findNetworkByEntityID_helper(const char *entityList, const long long maxDegree, const long long buildOutDegree, const long long maxEntities);
# _DLEXPORT struct G2_findNetworkByEntityID_V2_result G2_findNetworkByEntityID_V2_helper(const char *entityList, const long long maxDegree, const long long buildOutDegree, const long long maxEntities, long long flags);
# _DLEXPORT struct G2_findNetworkByRecordID_result G2_findNetworkByRecordID_helper(const char *recordList, const long long maxDegree, const long long buildOutDegree, const long long maxEntities);
# _DLEXPORT struct G2_findNetworkByRecordID_V2_result G2_findNetworkByRecordID_V2_helper(const char *recordList, const long long maxDegree, const long long buildOutDegree, const long long maxEntities, const long long flags);
# _DLEXPORT struct G2_findPathByEntityID_result G2_findPathByEntityID_helper(const long long entityID1, const long long entityID2, const long long maxDegree);
# _DLEXPORT struct G2_findPathByEntityID_V2_result G2_findPathByEntityID_V2_helper(const long long entityID1, const long long entityID2, const long long maxDegree, const long long flags);
# _DLEXPORT struct G2_findPathByRecordID_result G2_findPathByRecordID_helper(const char *dataSourceCode1, const char *recordID1, const char *dataSourceCode2, const char *recordID2, const long long maxDegree);
# _DLEXPORT struct G2_findPathByRecordID_V2_result G2_findPathByRecordID_V2_helper(const char *dataSourceCode1, const char *recordID1, const char *dataSourceCode2, const char *recordID2, const long long maxDegree, const long long flags);
# _DLEXPORT struct G2_findPathExcludingByEntityID_result G2_findPathExcludingByEntityID_helper(const long long entityID1, const long long entityID2, const long long maxDegree, const char *excludedEntities);
# _DLEXPORT struct G2_findPathExcludingByEntityID_V2_result G2_findPathExcludingByEntityID_V2_helper(const long long entityID1, const long long entityID2, const long long maxDegree, const char *excludedEntities, const long long flags);
# _DLEXPORT struct G2_findPathExcludingByRecordID_result G2_findPathExcludingByRecordID_helper(const char *dataSourceCode1, const char *recordID1, const char *dataSourceCode2, const char *recordID2, const long long maxDegree, const char *excludedRecords);
# _DLEXPORT struct G2_findPathExcludingByRecordID_V2_result G2_findPathExcludingByRecordID_V2_helper(const char *dataSourceCode1, const char *recordID1, const char *dataSourceCode2, const char *recordID2, const long long maxDegree, const char *excludedRecords, const long long flags);
# _DLEXPORT struct G2_findPathIncludingSourceByEntityID_result G2_findPathIncludingSourceByEntityID_helper(const long long entityID1, const long long entityID2, const long long maxDegree, const char *excludedEntities, const char *requiredDsrcs);
# _DLEXPORT struct G2_findPathIncludingSourceByEntityID_V2_result G2_findPathIncludingSourceByEntityID_V2_helper(const long long entityID1, const long long entityID2, const long long maxDegree, const char *excludedEntities, const char *requiredDsrcs, const long long flags);
# _DLEXPORT struct G2_findPathIncludingSourceByRecordID_result G2_findPathIncludingSourceByRecordID_helper(const char *dataSourceCode1, const char *recordID1, const char *dataSourceCode2, const char *recordID2, const long long maxDegree, const char *excludedRecords, const char *requiredDsrcs);
# _DLEXPORT struct G2_findPathIncludingSourceByRecordID_V2_result G2_findPathIncludingSourceByRecordID_V2_helper(const char *dataSourceCode1, const char *recordID1, const char *dataSourceCode2, const char *recordID2, const long long maxDegree, const char *excludedRecords, const char *requiredDsrcs, const long long flags);
# _DLEXPORT struct G2_fetchNext_result G2_fetchNext_helper(uintptr_t exportHandle);
# _DLEXPORT struct G2_getActiveConfigID_result G2_getActiveConfigID_helper();
# _DLEXPORT struct G2_getEntityByEntityID_result G2_getEntityByEntityID_helper(const long long entityID);
# _DLEXPORT struct G2_getEntityByEntityID_V2_result G2_getEntityByEntityID_V2_helper(const long long entityID, const long long flags);
# _DLEXPORT struct G2_getEntityByRecordID_result G2_getEntityByRecordID_helper(const char *dataSourceCode, const char *recordID);
# _DLEXPORT struct G2_getEntityByRecordID_V2_result G2_getEntityByRecordID_V2_helper(const char *dataSourceCode, const char *recordID, const long long flags);
# _DLEXPORT struct G2_getRecord_result G2_getRecord_helper(const char *dataSourceCode, const char *recordID);
# _DLEXPORT struct G2_getRecord_V2_result G2_getRecord_V2_helper(const char *dataSourceCode, const char *recordID, const long long flags);
# _DLEXPORT struct G2_getRedoRecord_result G2_getRedoRecord_helper();
# _DLEXPORT struct G2_getRepositoryLastModifiedTime_result G2_getRepositoryLastModifiedTime_helper();
# _DLEXPORT struct G2_getVirtualEntityByRecordID_result G2_getVirtualEntityByRecordID_helper(const char *recordList);
# _DLEXPORT struct G2_getVirtualEntityByRecordID_V2_result G2_getVirtualEntityByRecordID_V2_helper(const char *recordList, const long long flags);
# _DLEXPORT struct G2_howEntityByEntityID_result G2_howEntityByEntityID_helper(const long long entityID);
# _DLEXPORT struct G2_howEntityByEntityID_V2_result G2_howEntityByEntityID_V2_helper(const long long entityID, const long long flags);
# _DLEXPORT struct G2_processWithInfo_result G2_processWithInfo_helper(const char *record, const long long flags);
# _DLEXPORT struct G2_reevaluateEntityWithInfo_result G2_reevaluateEntityWithInfo_helper(const long long entityID, const long long flags);
# _DLEXPORT struct G2_reevaluateRecordWithInfo_result G2_reevaluateRecordWithInfo_helper(const char *dataSourceCode, const char *recordID, const long long flags);
# _DLEXPORT struct G2_replaceRecordWithInfo_result G2_replaceRecordWithInfo_helper(const char *dataSourceCode, const char *recordID, const char *jsonData, const char *loadID, const long long flags);
# _DLEXPORT struct G2_searchByAttributes_result G2_searchByAttributes_helper(const char *jsonData);
# _DLEXPORT struct G2_searchByAttributes_V2_result G2_searchByAttributes_V2_helper(const char *jsonData, const long long flags);
# _DLEXPORT struct G2_stats_result G2_stats_helper();
# _DLEXPORT struct G2_whyEntities_result G2_whyEntities_helper(const long long entityID1, const long long entityID2);
# _DLEXPORT struct G2_whyEntities_V2_result G2_whyEntities_V2_helper(const long long entityID1, const long long entityID2, const long long flags);
# _DLEXPORT struct G2_whyEntityByEntityID_result G2_whyEntityByEntityID_helper(const long long entityID1);
# _DLEXPORT struct G2_whyEntityByEntityID_V2_result G2_whyEntityByEntityID_V2_helper(const long long entityID1, const long long flags);
# _DLEXPORT struct G2_whyEntityByRecordID_result G2_whyEntityByRecordID_helper(const char *dataSourceCode, const char *recordID);
# _DLEXPORT struct G2_whyEntityByRecordID_V2_result G2_whyEntityByRecordID_V2_helper(const char *dataSourceCode, const char *recordID, const long long flags);
# _DLEXPORT struct G2_whyRecords_result G2_whyRecords_helper(const char *dataSourceCode1, const char *recordID1, const char *dataSourceCode2, const char *recordID2);
# _DLEXPORT struct G2_whyRecords_V2_result G2_whyRecords_V2_helper(const char *dataSourceCode1, const char *recordID1, const char *dataSourceCode2, const char *recordID2, const long long flags);
#




        #-----------------------------------------------------------------------------------------------------------------------------------------------------------



        #-----------------------------------------------------------------------------------------------------------------------------------------------------------
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------

        # Initialize Senzing engine.

        if len(module_name) > 0:
            self.init(self.module_name, self.ini_params, self.verbose_logging)

    def __del__(self) -> None:
        """Destructor"""
        self.destroy()

    # -------------------------------------------------------------------------
    # Development methods - to be removed after initial development
    # -------------------------------------------------------------------------

    def fake_g2engine(self, *args: Any, **kwargs: Any) -> None:
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
            self.library_handle.G2_getLastException,
            self.library_handle.G2_clearLastException,
            SENZING_PRODUCT_ID,
            error_id,
            self.ID_MESSAGES,
            CALLER_SKIP,
            *args,
        )

    # -------------------------------------------------------------------------
    # G2Engine methods
    # -------------------------------------------------------------------------

    def add_record(
        self,
        data_source_code: str,
        record_id: str,
        json_data: str,
        load_id: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.fake_g2engine(data_source_code, record_id, json_data, load_id)

    def add_record_with_info(
        self,
        data_source_code: str,
        record_id: str,
        json_data: str,
        load_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, json_data, load_id, flags)
        return "string"

    def close_export(self, response_handle: int, *args: Any, **kwargs: Any) -> None:
        self.fake_g2engine(response_handle)

    def count_redo_records(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2engine()
        return 0

    def delete_record(
        self,
        data_source_code: str,
        record_id: str,
        load_id: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.fake_g2engine(data_source_code, record_id, load_id)

    def delete_record_with_info(
        self,
        data_source_code: str,
        record_id: str,
        load_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, load_id, flags)
        return "string"

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        self.fake_g2engine()

    def export_config(self, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine()
        return "string"

    def export_config_and_config_id(self, *args: Any, **kwargs: Any) -> Tuple[str, int]:
        self.fake_g2engine()
        return "string", 0

    def export_csv_entity_report(
        self, csv_column_list: str, flags: int, *args: Any, **kwargs: Any
    ) -> int:
        self.fake_g2engine(csv_column_list, flags)
        return 0

    def export_json_entity_report(self, flags: int, *args: Any, **kwargs: Any) -> int:
        self.fake_g2engine(flags)
        return 0

    def fetch_next(self, response_handle: int, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine(response_handle)
        return "string"

    def find_interesting_entities_by_entity_id(
        self, entity_id: int, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(entity_id, flags)
        return "string"

    def find_interesting_entities_by_record_id(
        self,
        data_source_code: str,
        record_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def find_network_by_entity_id_v2(
        self,
        entity_list: str,
        max_degree: int,
        build_out_degree: int,
        max_entities: int,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            entity_list, max_degree, build_out_degree, max_entities, flags
        )
        return "string"

    def find_network_by_entity_id(
        self,
        entity_list: str,
        max_degree: int,
        build_out_degree: int,
        max_entities: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(entity_list, max_degree, build_out_degree, max_entities)
        return "string"

    def find_network_by_record_id_v2(
        self,
        record_list: str,
        max_degree: int,
        build_out_degree: int,
        max_entities: int,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            record_list, max_degree, build_out_degree, max_entities, flags
        )
        return "string"

    def find_network_by_record_id(
        self,
        record_list: str,
        max_degree: int,
        build_out_degree: int,
        max_entities: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(record_list, max_degree, build_out_degree, max_entities)
        return "string"

    def find_path_by_entity_id_v2(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(entity_id_1, entity_id_2, max_degree, flags)
        return "string"

    def find_path_by_entity_id(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(entity_id_1, entity_id_2, max_degree)
        return "string"

    def find_path_by_record_id_v2(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1,
            record_id_1,
            data_source_code_2,
            record_id_2,
            max_degree,
            flags,
        )
        return "string"

    def find_path_by_record_id(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1, record_id_1, data_source_code_2, record_id_2, max_degree
        )
        return "string"

    def find_path_excluding_by_entity_id_v2(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        excluded_entities: str,
        flags: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            entity_id_1, entity_id_2, max_degree, excluded_entities, flags
        )
        return "string"

    def find_path_excluding_by_entity_id(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        excluded_entities: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(entity_id_1, entity_id_2, max_degree, excluded_entities)
        return "string"

    def find_path_excluding_by_record_id_v2(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        excluded_records: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1,
            record_id_1,
            data_source_code_2,
            record_id_2,
            max_degree,
            excluded_records,
            flags,
        )
        return "string"

    def find_path_excluding_by_record_id(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        excluded_records: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1,
            record_id_1,
            data_source_code_2,
            record_id_2,
            max_degree,
            excluded_records,
        )
        return "string"

    def find_path_including_source_by_entity_id_v2(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        excluded_entities: str,
        required_dsrcs: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            entity_id_1,
            entity_id_2,
            max_degree,
            excluded_entities,
            required_dsrcs,
            flags,
        )
        return "string"

    def find_path_including_source_by_entity_id(
        self,
        entity_id_1: int,
        entity_id_2: int,
        max_degree: int,
        excluded_entities: str,
        required_dsrcs: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            entity_id_1, entity_id_2, max_degree, excluded_entities, required_dsrcs
        )
        return "string"

    def find_path_including_source_by_record_id_v2(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        excluded_records: str,
        required_dsrcs: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1,
            record_id_1,
            data_source_code_2,
            record_id_2,
            max_degree,
            excluded_records,
            required_dsrcs,
            flags,
        )
        return "string"

    def find_path_including_source_by_record_id(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        max_degree: int,
        excluded_records: str,
        required_dsrcs: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1,
            record_id_1,
            data_source_code_2,
            record_id_2,
            max_degree,
            excluded_records,
            required_dsrcs,
        )
        return "string"

    def get_active_config_id(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2engine()
        return 0

    def get_entity_by_entity_id_v2(
        self, entity_id: int, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(entity_id, flags)
        return "string"

    def get_entity_by_entity_id(self, entity_id: int, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine(entity_id)
        return "string"

    def get_entity_by_record_id_v2(
        self,
        data_source_code: str,
        record_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def get_entity_by_record_id(
        self, data_source_code: str, record_id: str, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(data_source_code, record_id)
        return "string"

    def get_record_v2(
        self,
        data_source_code: str,
        record_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def get_record(
        self, data_source_code: str, record_id: str, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(data_source_code, record_id)
        return "string"

    def get_redo_record(self, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine()
        return "string"

    def get_repository_last_modified_time(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2engine()
        return 0

    def get_virtual_entity_by_record_id_v2(
        self, record_list: str, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(record_list, flags)
        return "string"

    def get_virtual_entity_by_record_id(
        self, record_list: str, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(record_list)
        return "string"

    def how_entity_by_entity_id_v2(
        self, entity_id: int, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(entity_id, flags)
        return "string"

    def how_entity_by_entity_id(self, entity_id: int, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine(entity_id)
        return "string"

    def init(
        self,
        module_name: str,
        ini_params: str,
        verbose_logging: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.fake_g2engine(module_name, ini_params, verbose_logging)

    def init_with_config_id(
        self,
        module_name: str,
        ini_params: str,
        init_config_id: int,
        verbose_logging: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.fake_g2engine(module_name, ini_params, init_config_id, verbose_logging)

    def prime_engine(self, *args: Any, **kwargs: Any) -> None:
        self.fake_g2engine()

    def process(self, record: str, *args: Any, **kwargs: Any) -> None:
        self.fake_g2engine(record)

    def process_with_info(
        self, record: str, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(record, flags)
        return "string"

    def purge_repository(self, *args: Any, **kwargs: Any) -> None:
        self.fake_g2engine()

    def reevaluate_entity(
        self, entity_id: int, flags: int, *args: Any, **kwargs: Any
    ) -> None:
        self.fake_g2engine(entity_id, flags)

    def reevaluate_entity_with_info(
        self, entity_id: int, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(entity_id, flags)
        return "string"

    def reevaluate_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.fake_g2engine(data_source_code, record_id, flags)

    def reevaluate_record_with_info(
        self,
        data_source_code: str,
        record_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def reinit(self, init_config_id: int, *args: Any, **kwargs: Any) -> None:
        self.fake_g2engine(init_config_id)

    def replace_record(
        self,
        data_source_code: str,
        record_id: str,
        json_data: str,
        load_id: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.fake_g2engine(data_source_code, record_id, json_data, load_id)

    def replace_record_with_info(
        self,
        data_source_code: str,
        record_id: str,
        json_data: str,
        load_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, json_data, load_id, flags)
        return "string"

    def search_by_attributes_v2(
        self, json_data: str, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(json_data, flags)
        return "string"

    def search_by_attributes(self, json_data: str, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine(json_data)
        return "string"

    def stats(self, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine()
        return "string"

    def why_entities_v2(
        self, entity_id_1: int, entity_id_2: int, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(entity_id_1, entity_id_2, flags)
        return "string"

    def why_entities(
        self, entity_id_1: int, entity_id_2: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(entity_id_1, entity_id_2)
        return "string"

    def why_entity_by_entity_id_v2(
        self, entity_id: str, flags: int, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(entity_id, flags)
        return "string"

    def why_entity_by_entity_id(self, entity_id: int, *args: Any, **kwargs: Any) -> str:
        self.fake_g2engine(entity_id)
        return "string"

    def why_entity_by_record_id_v2(
        self,
        data_source_code: str,
        record_id: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(data_source_code, record_id, flags)
        return "string"

    def why_entity_by_record_id(
        self, data_source_code: str, record_id: str, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2engine(data_source_code, record_id)
        return "string"

    def why_records_v2(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        flags: int,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1, record_id_1, data_source_code_2, record_id_2, flags
        )
        return "string"

    def why_records(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        self.fake_g2engine(
            data_source_code_1, record_id_1, data_source_code_2, record_id_2
        )
        return "string"
