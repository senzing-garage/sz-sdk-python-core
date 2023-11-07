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

# pylint: disable=R0903,C0302,R0915

import os
from ctypes import (
    POINTER,
    Structure,
    c_char,
    c_char_p,
    c_int,
    c_longlong,
    c_size_t,
    c_uint,
    c_void_p,
    cdll,
)
from typing import Any, Tuple

from .g2engine_abstract import G2EngineAbstract
from .g2exception import G2Exception, new_g2exception
from .g2helpers import find_file_in_path

# Metadata

__all__ = ["G2Engine"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-02"

SENZING_PRODUCT_ID = "5043"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md
CALLER_SKIP = 6  # Number of stack frames to skip when reporting location in Exception.

# -----------------------------------------------------------------------------
# Classes that are result structures from calls to Senzing
# -----------------------------------------------------------------------------


class G2ResponseReturnCodeResult(Structure):
    """Simple response, return_code structure"""

    _fields_ = [
        ("response", POINTER(c_char)),
        ("return_code", c_longlong),
    ]


class G2AddRecordWithInfoResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_addRecordWithInfo_result"""


class G2DeleteRecordWithInfoResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_deleteRecordWithInfo_result"""


class G2ExportConfigAndConfigIDResult(Structure):
    """In golang_helpers.h G2_exportConfigAndConfigID_result"""

    _fields_ = [
        ("config_id", c_longlong),
        ("config", POINTER(c_char)),
        ("return_code", c_longlong),
    ]


class G2ExportConfigResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_exportConfig_result"""


class G2ExportCSVEntityReportResult(Structure):
    """In golang_helpers.h G2_exportCSVEntityReport_result"""

    _fields_ = [
        ("export_handle", c_void_p),
        ("return_code", c_longlong),
    ]


class G2ExportJSONEntityReportResult(Structure):
    """In golang_helpers.h G2_exportJSONEntityReport_result"""

    _fields_ = [
        ("export_handle", c_void_p),
        ("return_code", c_longlong),
    ]


class G2FetchNextResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_fetchNext_result"""


class G2FindInterestingEntitiesByEntityIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findInterestingEntitiesByEntityID_result"""


class G2FindInterestingEntitiesByRecordIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findInterestingEntitiesByRecordID_result"""


class G2FindNetworkByEntityIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findNetworkByEntityID_result"""


class G2FindNetworkByEntityIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findNetworkByEntityID_V2_result"""


class G2FindNetworkByRecordIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findNetworkByRecordID_result"""


class G2FindNetworkByRecordIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findNetworkByRecordID_V2_result"""


class G2FindPathByEntityIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findPathByEntityID_result"""


class G2FindPathByEntityIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findPathByEntityID_V2_result"""


class G2FindPathByRecordIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findPathByRecordID_result"""


class G2FindPathByRecordIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findPathByRecordID_V2_result"""


class G2FindPathExcludingByEntityIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findPathExcludingByEntityID_result"""


class G2FindPathExcludingByEntityIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findPathExcludingByEntityID_V2_result"""


class G2FindPathExcludingByRecordIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findPathExcludingByRecordID_result"""


class G2FindPathExcludingByRecordIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findPathExcludingByRecordID_V2_result"""


class G2FindPathIncludingSourceByEntityIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findPathIncludingSourceByEntityID_result"""


class G2FindPathIncludingSourceByEntityIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findPathIncludingSourceByEntityID_V2_result"""


class G2FindPathIncludingSourceByRecordIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findPathIncludingSourceByRecordID_result"""


class G2FindPathIncludingSourceByRecordIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_findPathIncludingSourceByRecordID_V2_result"""


class G2GetActiveConfigIDResult(Structure):
    """In golang_helpers.h G2_getActiveConfigID_result"""

    _fields_ = [
        ("config_id", c_longlong),
        ("return_code", c_longlong),
    ]


class G2GetEntityByEntityIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_getEntityByEntityID_result"""


class G2GetEntityByEntityIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_getEntityByEntityID_V2_result"""


class G2GetEntityByRecordIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_getEntityByRecordID_result"""


class G2GetEntityByRecordIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_getEntityByRecordID_V2_result"""


class G2GetRecordResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_getRecord_result"""


class G2GetRecordV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_getRecord_V2_result"""


class G2GetRedoRecordResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_getRedoRecord_result"""


class G2GetRepositoryLastModifiedTimeResult(Structure):
    """In golang_helpers.h G2_getRepositoryLastModifiedTime_result"""

    _fields_ = [
        ("time", c_longlong),
        ("return_code", c_longlong),
    ]


class G2GetVirtualEntityByRecordIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_getVirtualEntityByRecordID_result"""


class G2GetVirtualEntityByRecordIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_getVirtualEntityByRecordID_V2_result"""


class G2HowEntityByEntityIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_howEntityByEntityID_result"""


class G2HowEntityByEntityIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_howEntityByEntityID_V2_result"""


class G2ProcessWithInfoResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_processWithInfo_result"""


class G2ReevaluateEntityWithInfoResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_reevaluateEntityWithInfo_result"""


class G2ReevaluateRecordWithInfoResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_reevaluateRecordWithInfo_result"""


class G2ReplaceRecordWithInfoResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_replaceRecordWithInfo_result"""


class G2SearchByAttributesResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_searchByAttributes_result"""


class G2SearchByAttributesV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_searchByAttributes_V2_result"""


class G2StatsResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_stats_result"""


class G2WhyEntitiesResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_whyEntities_result"""


class G2WhyEntitiesV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_whyEntities_V2_result"""


class G2WhyEntityByEntityIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_whyEntityByEntityID_result"""


class G2WhyEntityByEntityIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_whyEntityByEntityID_V2_result"""


class G2WhyEntityByRecordIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_whyEntityByRecordID_result"""


class G2WhyEntityByRecordIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_whyEntityByRecordID_V2_result"""


class G2WhyRecordsResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_whyRecords_result"""


class G2WhyRecordsV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_whyRecords_V2_result"""


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

        g2_engine = g2engine.G2Engine(MODULE_NAME, INI_PARAMS)


    If the G2Engine constructor is called without parameters,
    the `init()` method must be called to initialize the use of G2Engine.

    Example:

    .. code-block:: python

        g2_engine = g2engine.G2Engine()
        g2_engine.init(MODULE_NAME, INI_PARAMS, ENGINE_VERBOSE_LOGGING)

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
        G2Exception: Raised when input parameters are incorrect.

    .. collapse:: Example:

        .. literalinclude:: ../../examples/g2engine/g2engine_constructor.py
            :linenos:
            :language: python
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
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
        self.noop = ""
        self.verbose_logging = verbose_logging

        # Load binary library.

        try:
            if os.name == "nt":
                self.library_handle = cdll.LoadLibrary(find_file_in_path("G2.dll"))
            else:
                self.library_handle = cdll.LoadLibrary("libG2.so")
        except OSError as err:
            raise G2Exception("Failed to load the G2 library") from err

        # Initialize C function input parameters and results.
        # Must be synchronized with g2/sdk/c/libg2engine.h

        self.library_handle.G2_addRecord.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
        ]
        self.library_handle.G2_addRecord.restype = c_int
        # self.library_handle.G2_addRecordWithInfo.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_addRecordWithInfo_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_addRecordWithInfo_helper.restype = (
            G2AddRecordWithInfoResult
        )
        # self.library_handle.G2_addRecordWithInfoWithReturnedRecordID.argtypes = [c_char_p, c_char_p, c_char_p, c_longlong, c_char_p, c_size_t, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def3]
        # self.library_handle.G2_addRecordWithInfoWithReturnedRecordID.restype = c_int
        # self.library_handle.G2_addRecordWithReturnedRecordID.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_size_t]
        # self.library_handle.G2_checkRecord.argtypes = [ c_char_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_clearLastException.argtypes = []
        self.library_handle.G2_clearLastException.restype = None
        # self.library_handle.G2_closeExport.argtypes = [c_void_p]
        # self.library_handle.G2_closeExport.restype = c_int
        self.library_handle.G2_closeExport_helper.argtypes = [
            POINTER(c_uint),
        ]  # TODO: This may not be correct.
        self.library_handle.G2_closeExport_helper.restype = c_longlong
        # self.library_handle.G2_deleteRecordWithInfo.argtypes = [c_char_p, c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_deleteRecordWithInfo_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_deleteRecordWithInfo_helper.restype = (
            G2DeleteRecordWithInfoResult
        )
        # self.library_handle.G2_exportConfig.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_exportConfig_helper.argtypes = []
        self.library_handle.G2_exportConfig_helper.restype = G2ExportConfigResult
        self.library_handle.G2_exportConfigAndConfigID_helper.argtypes = []
        self.library_handle.G2_exportConfigAndConfigID_helper.restype = (
            G2ExportConfigAndConfigIDResult
        )
        # self.library_handle.G2_exportCSVEntityReport.argtypes = [c_char_p, c_longlong, POINTER(c_void_p)]
        # self.library_handle.G2_exportCSVEntityReport.restype = c_int
        self.library_handle.G2_exportCSVEntityReport_helper.argtypes = [
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_exportCSVEntityReport_helper.restype = (
            G2ExportCSVEntityReportResult
        )
        # self.library_handle.G2_exportJSONEntityReport.argtypes = [c_longlong, POINTER(c_void_p)]
        # self.library_handle.G2_exportJSONEntityReport.restype = c_int
        self.library_handle.G2_exportJSONEntityReport_helper.argtypes = [c_longlong]
        self.library_handle.G2_exportJSONEntityReport_helper.restype = (
            G2ExportJSONEntityReportResult
        )
        # self.library_handle.G2_fetchNext.argtypes = [c_void_p, c_char_p, c_size_t]
        # self.library_handle.G2_fetchNext.restype = c_int
        self.library_handle.G2_fetchNext_helper.argtypes = [
            POINTER(c_uint),
        ]  # TODO: This may not be correct.
        self.library_handle.G2_fetchNext_helper.restype = G2FetchNextResult
        # self.library_handle.G2_findInterestingEntitiesByEntityID.argtypes = [c_longlong, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_findInterestingEntitiesByEntityID.restype = c_int
        self.library_handle.G2_findInterestingEntitiesByEntityID_helper.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2_findInterestingEntitiesByEntityID_helper.restype = (
            G2FindInterestingEntitiesByEntityIDResult
        )
        # self.library_handle.G2_findInterestingEntitiesByRecordID.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_findInterestingEntitiesByRecordID.restype = c_int
        self.library_handle.G2_findInterestingEntitiesByRecordID_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_findInterestingEntitiesByRecordID_helper.restype = (
            G2FindInterestingEntitiesByRecordIDResult
        )
        self.library_handle.G2_findNetworkByEntityID_helper.argtypes = [
            c_char_p,
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2_findNetworkByEntityID_helper.restype = (
            G2FindNetworkByEntityIDResult
        )
        # self.library_handle.G2_findNetworkByEntityID_V2.argtypes = [c_char_p, c_int, c_int, c_int, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_findNetworkByEntityID_V2.restype = c_int
        self.library_handle.G2_findNetworkByEntityID_V2_helper.argtypes = [
            c_char_p,
            c_longlong,
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2_findNetworkByEntityID_V2_helper.restype = (
            G2FindNetworkByEntityIDV2Result
        )
        self.library_handle.G2_findNetworkByRecordID_helper.argtypes = [
            c_char_p,
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2_findNetworkByRecordID_helper.restype = (
            G2FindNetworkByRecordIDResult
        )
        # self.library_handle.G2_findNetworkByRecordID_V2.argtypes = [c_char_p, c_int, c_int, c_int, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_findNetworkByRecordID_V2.restype = c_int
        self.library_handle.G2_findNetworkByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_longlong,
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2_findNetworkByRecordID_V2_helper.restype = (
            G2FindNetworkByRecordIDV2Result
        )
        self.library_handle.G2_findPathByEntityID_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2_findPathByEntityID_helper.restype = (
            G2FindPathByEntityIDResult
        )
        # self.library_handle.G2_findPathByEntityID_V2.argtypes = [c_longlong, c_longlong, c_int, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_findPathByEntityID_V2.restype = c_int
        self.library_handle.G2_findPathByEntityID_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2_findPathByEntityID_V2_helper.restype = (
            G2FindPathByEntityIDV2Result
        )
        self.library_handle.G2_findPathByRecordID_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_findPathByRecordID_helper.restype = (
            G2FindPathByRecordIDResult
        )
        # self.library_handle.G2_findPathByRecordID_V2.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_findPathByRecordID_V2.restype = c_int
        self.library_handle.G2_findPathByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2_findPathByRecordID_V2_helper.restype = (
            G2FindPathByRecordIDV2Result
        )
        self.library_handle.G2_findPathExcludingByEntityID_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
            c_char_p,
        ]
        self.library_handle.G2_findPathExcludingByEntityID_helper.restype = (
            G2FindPathExcludingByEntityIDResult
        )
        # self.library_handle.G2_findPathExcludingByEntityID_V2.argtypes = [c_longlong, c_longlong, c_int, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_findPathExcludingByEntityID_V2.restype = c_int
        self.library_handle.G2_findPathExcludingByEntityID_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_findPathExcludingByEntityID_V2_helper.restype = (
            G2FindPathExcludingByEntityIDV2Result
        )
        self.library_handle.G2_findPathExcludingByRecordID_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
            c_char_p,
        ]
        self.library_handle.G2_findPathExcludingByRecordID_helper.restype = (
            G2FindPathExcludingByRecordIDResult
        )
        # self.library_handle.G2_findPathExcludingByRecordID_V2.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_findPathExcludingByRecordID_V2.restype = c_int
        self.library_handle.G2_findPathExcludingByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_findPathExcludingByRecordID_V2_helper.restype = (
            G2FindPathExcludingByRecordIDV2Result
        )
        self.library_handle.G2_findPathIncludingSourceByEntityID_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
            c_char_p,
            c_char_p,
        ]
        self.library_handle.G2_findPathIncludingSourceByEntityID_helper.restype = (
            G2FindPathIncludingSourceByEntityIDResult
        )
        # self.library_handle.G2_findPathIncludingSourceByEntityID_V2.argtypes = [c_longlong, c_longlong, c_int, c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_findPathIncludingSourceByEntityID_V2.restype = c_int
        self.library_handle.G2_findPathIncludingSourceByEntityID_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_findPathIncludingSourceByEntityID_V2_helper.restype = (
            G2FindPathIncludingSourceByEntityIDV2Result
        )
        self.library_handle.G2_findPathIncludingSourceByRecordID_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
            c_char_p,
            c_char_p,
        ]
        self.library_handle.G2_findPathIncludingSourceByRecordID_helper.restype = (
            G2FindPathIncludingSourceByRecordIDResult
        )
        # self.library_handle.G2_findPathIncludingSourceByRecordID_V2.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_findPathIncludingSourceByRecordID_V2.restype = c_int
        self.library_handle.G2_findPathIncludingSourceByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_findPathIncludingSourceByRecordID_V2_helper.restype = (
            G2FindPathIncludingSourceByRecordIDV2Result
        )
        # self.library_handle.G2_getActiveConfigID.argtypes = [POINTER(c_longlong)]
        self.library_handle.G2_getActiveConfigID_helper.argtypes = []
        self.library_handle.G2_getActiveConfigID_helper.restype = (
            G2GetActiveConfigIDResult
        )
        self.library_handle.G2_getEntityByEntityID_helper.argtypes = [c_longlong]
        self.library_handle.G2_getEntityByEntityID_helper.restype = (
            G2GetEntityByEntityIDResult
        )
        # self.library_handle.G2_getEntityByEntityID_V2.argtypes = [c_longlong, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_getEntityByEntityID_V2.restype = c_int
        self.library_handle.G2_getEntityByEntityID_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2_getEntityByEntityID_V2_helper.restype = (
            G2GetEntityByEntityIDV2Result
        )
        self.library_handle.G2_getEntityByRecordID_helper.argtypes = [
            c_char_p,
            c_char_p,
        ]
        self.library_handle.G2_getEntityByRecordID_helper.restype = (
            G2GetEntityByRecordIDResult
        )
        # self.library_handle.G2_getEntityByRecordID_V2.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_getEntityByRecordID_V2.restype = c_int
        self.library_handle.G2_getEntityByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_getEntityByRecordID_V2_helper.restype = (
            G2GetEntityByRecordIDV2Result
        )
        self.library_handle.G2_getLastException.argtypes = [
            POINTER(c_char),
            c_size_t,
        ]
        self.library_handle.G2_getLastException.restype = c_longlong
        self.library_handle.G2_getLastExceptionCode.argtypes = []
        self.library_handle.G2_getLastExceptionCode.restype = c_int
        self.library_handle.G2_getRecord_helper.argtypes = [c_char_p, c_char_p]
        self.library_handle.G2_getRecord_helper.restype = G2GetRecordResult
        # self.library_handle.G2_getRecord_V2.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_getRecord_V2.restype = c_int
        self.library_handle.G2_getRecord_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_getRecord_V2_helper.restype = G2GetRecordV2Result
        # self.library_handle.G2_getRedoRecord.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_getRedoRecord.restype = c_int
        self.library_handle.G2_getRedoRecord_helper.argtypes = []
        self.library_handle.G2_getRedoRecord_helper.restype = G2GetRedoRecordResult
        # self.library_handle.G2_getRepositoryLastModifiedTime.argtypes = [POINTER(c_longlong)]
        self.library_handle.G2_getRepositoryLastModifiedTime_helper.argtypes = []
        self.library_handle.G2_getRepositoryLastModifiedTime_helper.restype = (
            G2GetRepositoryLastModifiedTimeResult
        )
        self.library_handle.G2_getVirtualEntityByRecordID_helper.argtypes = [c_char_p]
        self.library_handle.G2_getVirtualEntityByRecordID_helper.restype = (
            G2GetVirtualEntityByRecordIDResult
        )
        # self.library_handle.G2_getVirtualEntityByRecordID_V2.argtypes = [c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_getVirtualEntityByRecordID_V2.restype = c_int
        self.library_handle.G2_getVirtualEntityByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_getVirtualEntityByRecordID_V2_helper.restype = (
            G2GetVirtualEntityByRecordIDV2Result
        )
        self.library_handle.G2_howEntityByEntityID_helper.argtypes = [c_longlong]
        self.library_handle.G2_howEntityByEntityID_helper.restype = (
            G2HowEntityByEntityIDResult
        )
        # self.library_handle.G2_howEntityByEntityID_V2.argtypes = [c_longlong, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_howEntityByEntityID_V2.restype = c_int
        self.library_handle.G2_howEntityByEntityID_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2_howEntityByEntityID_V2_helper.restype = (
            G2HowEntityByEntityIDV2Result
        )
        self.library_handle.G2_init.argtypes = [c_char_p, c_char_p, c_int]
        self.library_handle.G2_initWithConfigID.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
            c_int,
        ]
        self.library_handle.G2_process.argtypes = [c_char_p]
        self.library_handle.G2_process.restype = c_int
        # self.library_handle.G2_processRedoRecord.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_processRedoRecord.restype = c_int
        # self.library_handle.G2_processWithInfo.argtypes = [c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_processWithInfo_helper.argtypes = [c_char_p, c_longlong]
        self.library_handle.G2_processWithInfo_helper.restype = G2ProcessWithInfoResult
        # self.library_handle.G2_processWithResponseResize.argtypes = [c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_reevaluateEntity.argtypes = [c_longlong, c_longlong]
        # self.library_handle.G2_reevaluateEntityWithInfo.argtypes = [c_int, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_reevaluateEntityWithInfo_helper.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2_reevaluateEntityWithInfo_helper.restype = (
            G2ReevaluateEntityWithInfoResult
        )
        self.library_handle.G2_reevaluateRecord.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_reevaluateRecord.restype = c_int
        # self.library_handle.G2_reevaluateRecordWithInfo.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_reevaluateRecordWithInfo_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_reevaluateRecordWithInfo_helper.restype = (
            G2ReevaluateRecordWithInfoResult
        )
        self.library_handle.G2_reinit.argtypes = [c_longlong]
        # self.library_handle.G2_replaceRecordWithInfo.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_replaceRecordWithInfo_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_replaceRecordWithInfo_helper.restype = (
            G2ReplaceRecordWithInfoResult
        )
        self.library_handle.G2_searchByAttributes_helper.argtypes = [c_char_p]
        self.library_handle.G2_searchByAttributes_helper.restype = (
            G2SearchByAttributesResult
        )
        # self.library_handle.G2_searchByAttributes_V2.argtypes = [c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_searchByAttributes_V2_helper.argtypes = [
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_searchByAttributes_V2_helper.restype = (
            G2SearchByAttributesV2Result
        )
        # self.library_handle.G2_searchByAttributes_V3.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_stats.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_stats_helper.argtypes = []
        self.library_handle.G2_stats_helper.restype = G2StatsResult
        self.library_handle.G2_whyEntities_helper.argtypes = [c_longlong, c_longlong]
        self.library_handle.G2_whyEntities_helper.restype = G2WhyEntitiesResult
        # self.library_handle.G2_whyEntities_V2.argtypes = [c_longlong, c_longlong, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_whyEntities_V2.restype = c_int
        self.library_handle.G2_whyEntities_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2_whyEntities_V2_helper.restype = G2WhyEntitiesV2Result
        self.library_handle.G2_whyEntityByEntityID_helper.argtypes = [c_longlong]
        self.library_handle.G2_whyEntityByEntityID_helper.restype = (
            G2WhyEntityByEntityIDResult
        )
        # self.library_handle.G2_whyEntityByEntityID_V2.argtypes = [c_longlong, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_whyEntityByEntityID_V2.restype = c_int
        self.library_handle.G2_whyEntityByEntityID_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2_whyEntityByEntityID_V2_helper.restype = (
            G2WhyEntityByEntityIDV2Result
        )
        self.library_handle.G2_whyEntityByRecordID_helper.argtypes = [
            c_char_p,
            c_char_p,
        ]
        self.library_handle.G2_whyEntityByRecordID_helper.restype = (
            G2WhyEntityByRecordIDResult
        )
        # self.library_handle.G2_whyEntityByRecordID_V2.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_whyEntityByRecordID_V2.restype = c_int
        self.library_handle.G2_whyEntityByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_whyEntityByRecordID_V2_helper.restype = (
            G2WhyEntityByRecordIDV2Result
        )
        # self.library_handle.G2_whyRecordInEntity_V2.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_whyRecordInEntity_V2.restype = c_int
        self.library_handle.G2_whyRecords_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
        ]
        self.library_handle.G2_whyRecords_helper.restype = G2WhyRecordsResult
        # self.library_handle.G2_whyRecords_V2.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_whyRecords_V2.restype = c_int
        self.library_handle.G2_whyRecords_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_whyRecords_V2_helper.restype = G2WhyRecordsV2Result
        self.library_handle.G2GoHelper_free.argtypes = [c_char_p]

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
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        self.fake_g2engine(module_name, ini_params, verbose_logging)

    def init_with_config_id(
        self,
        module_name: str,
        ini_params: str,
        init_config_id: int,
        verbose_logging: int = 0,
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
