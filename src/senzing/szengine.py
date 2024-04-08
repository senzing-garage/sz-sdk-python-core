"""
The g2engine package is used to insert, update, delete and query records and entities in the Senzing product.
It is a wrapper over Senzing's G2Engine C binding.
It conforms to the interface specified in
`g2engine_abstract.py <https://github.com/senzing-garage/g2-sdk-python-next/blob/main/src/senzing/g2engine_abstract.py>`_

# TODO: Also pythonpath and engine vars?
To use g2engine,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/g2/lib
"""

# pylint: disable=R0903,C0302,R0915
# AC - Temp disables to get changes in for move to senzing garage
# pylint: disable=W0511,W1113,W0613
# NOTE Used for ctypes type hinting - https://stackoverflow.com/questions/77619149/python-ctypes-pointer-type-hinting
from __future__ import annotations

import os
from ctypes import (
    POINTER,
    Structure,
    c_char,
    c_char_p,
    c_int,
    c_longlong,
    c_uint,
    c_void_p,
    cdll,
)
from typing import Any, Dict, Optional

from .szengine_abstract import SzEngineAbstract
from .szengineflags import SzEngineFlags
from .szexception import SzException, new_szexception
from .szhelpers import (
    FreeCResources,
    as_c_char_p,
    as_python_int,
    as_python_str,
    as_str,
    as_uintptr_t,
    catch_ctypes_exceptions,
    find_file_in_path,
)
from .szversion import is_supported_senzingapi_version

# Metadata

__all__ = ["SzEngine"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-15"

SENZING_PRODUCT_ID = "5043"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md

# FIXME CALLER_SKIP = 6  # Number of stack frames to skip when reporting location in Exception.
# TODO Investigate the error messages not showing correct location, because of wrapped methods?
CALLER_SKIP = 5  # Number of stack frames to skip when reporting location in Exception.

# # -----------------------------------------------------------------------------
# # Helper Classes
# # -----------------------------------------------------------------------------
# class AsDict(str):
#     """ """

#     def __init__(self, json_string: str):
#         self.json_string = json_string

#     # json.loads() is always Any
#     def as_dict(self) -> Any:
#         return json.loads(self.json_string)


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


class G2GetActiveConfigIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_getActiveConfigID_result"""


class G2GetEntityByEntityIDResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_getEntityByEntityID_result"""


class G2GetEntityByEntityIDV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_getEntityByEntityID_V2_result"""


class G2GetEntityByRecordIDResult(Structure):
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


class G2ProcessRedoRecordWithInfoResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_processRedoRecordWithInfo_result"""


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


class G2SearchByAttributesV3Result(G2ResponseReturnCodeResult):
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


class G2WhyRecordInEntityV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_whyRecordInEntity_V2_result"""


class G2WhyRecordsResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_whyRecords_result"""


class G2WhyRecordsV2Result(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2_whyRecords_V2_result"""


# -----------------------------------------------------------------------------
# G2Engine class
# -----------------------------------------------------------------------------


# TODO init_config_id ?
# TODO Optional on Parameters needs to be explained for different init methods
# TODO Raises could be more granular
class SzEngine(SzEngineAbstract):
    """
    The `init` method initializes the Senzing G2Engine object.
    It must be called prior to any other calls.

    **Note:** If the G2Engine constructor is called with parameters,
    the constructor will automatically call the `init()` method.

    Example:

    .. code-block:: python

        g2_engine = g2engine.G2Engine(module_name, ini_params)


    If the G2Engine constructor is called without parameters,
    the `init()` method must be called to initialize the use of G2Engine.

    Example:

    .. code-block:: python

        g2_engine = g2engine.G2Engine()
        g2_engine.init(module_name, ini_params, verbose_logging)

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
    # TODO Check all error codes

    def __init__(
        self,
        instance_name: str = "",
        settings: str | Dict[Any, Any] = "",
        verbose_logging: int = 0,
        config_id: int = 0,
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
        self.noop = ""
        self.verbose_logging = verbose_logging

        # Determine if Senzing API version is acceptable.

        is_supported_senzingapi_version()

        # Load binary library.

        try:
            if os.name == "nt":
                self.library_handle = cdll.LoadLibrary(find_file_in_path("G2.dll"))
            else:
                self.library_handle = cdll.LoadLibrary("libG2.so")
        except OSError as err:
            # TODO Additional explanation e.g. is LD_LIBRARY_PATH set
            raise SzException("Failed to load the G2 library") from err

        # Initialize C function input parameters and results.
        # Must be synchronized with g2/sdk/c/libg2engine.h

        self.library_handle.G2_addRecord.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            # c_char_p,
        ]
        self.library_handle.G2_addRecord.restype = c_int
        # self.library_handle.G2_addRecordWithInfo.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        self.library_handle.G2_addRecordWithInfo_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            # c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_addRecordWithInfo_helper.restype = (
            G2AddRecordWithInfoResult
        )
        # self.library_handle.G2_addRecordWithInfoWithReturnedRecordID.argtypes = [c_char_p, c_char_p, c_char_p, c_longlong, c_char_p, c_size_t, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def3]
        # self.library_handle.G2_addRecordWithInfoWithReturnedRecordID.restype = c_int
        # self.library_handle.G2_addRecordWithReturnedRecordID.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_size_t]
        # self.library_handle.G2_checkRecord.argtypes = [ c_char_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # TODO Remove
        # self.library_handle.G2_clearLastException.argtypes = []
        # self.library_handle.G2_clearLastException.restype = None
        # self.library_handle.G2_closeExport.argtypes = [c_void_p]
        # self.library_handle.G2_closeExport.restype = c_int
        self.library_handle.G2_closeExport_helper.argtypes = [
            POINTER(c_uint),
        ]
        self.library_handle.G2_closeExport_helper.restype = c_longlong
        # NOTE Added
        self.library_handle.G2_countRedoRecords.argtypes = []
        self.library_handle.G2_countRedoRecords.restype = c_longlong
        self.library_handle.G2_deleteRecord.argtypes = [
            c_char_p,
            c_char_p,
            # c_char_p,
        ]
        self.library_handle.G2_deleteRecord.restype = c_int
        self.library_handle.G2_deleteRecordWithInfo_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_deleteRecordWithInfo_helper.restype = (
            G2DeleteRecordWithInfoResult
        )
        self.library_handle.G2_destroy.argtypes = []
        self.library_handle.G2_destroy.restype = c_longlong
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
        ]
        self.library_handle.G2_fetchNext_helper.restype = G2FetchNextResult
        # self.library_handle.G2_findInterestingEntitiesByEntityID.argtypes = [c_longlong, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2_findInterestingEntitiesByEntityID.restype = c_int
        # TODO Completely remove?
        # self.library_handle.G2_findInterestingEntitiesByEntityID_helper.argtypes = [
        #     c_longlong,
        #     c_longlong,
        # ]
        # self.library_handle.G2_findInterestingEntitiesByEntityID_helper.restype = (
        #     G2FindInterestingEntitiesByEntityIDResult
        # )
        # # self.library_handle.G2_findInterestingEntitiesByRecordID.argtypes = [c_char_p, c_char_p, c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # # self.library_handle.G2_findInterestingEntitiesByRecordID.restype = c_int
        # self.library_handle.G2_findInterestingEntitiesByRecordID_helper.argtypes = [
        #     c_char_p,
        #     c_char_p,
        #     c_longlong,
        # ]
        # self.library_handle.G2_findInterestingEntitiesByRecordID_helper.restype = (
        #     G2FindInterestingEntitiesByRecordIDResult
        # )
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
        self.library_handle.G2_getEntityByEntityID_helper.argtypes = [
            c_longlong,
            c_longlong,
        ]
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
        # self.library_handle.G2_getLastException.argtypes = [
        #     POINTER(c_char),
        #     c_size_t,
        # ]
        # TODO Remove
        # self.library_handle.G2_getLastException.restype = c_longlong
        # self.library_handle.G2_getLastExceptionCode.argtypes = []
        # self.library_handle.G2_getLastExceptionCode.restype = c_int
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
        self.library_handle.G2_processRedoRecord.argtypes = [
            c_char_p,
        ]
        self.library_handle.G2_processRedoRecord.restype = c_int
        self.library_handle.G2_processRedoRecordWithInfo_helper.argtypes = [
            c_char_p,
        ]
        self.library_handle.G2_processRedoRecordWithInfo_helper.restype = (
            G2ProcessRedoRecordWithInfoResult
        )
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
        self.library_handle.G2_searchByAttributes_V3_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_searchByAttributes_V3_helper.restype = (
            G2SearchByAttributesV3Result
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

        self.library_handle.G2_whyRecordInEntity_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.G2_whyRecordInEntity_V2_helper.restype = (
            G2WhyRecordInEntityV2Result
        )

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

        # TODO Need to add in config_id
        # Optionally, initialize Senzing engine.
        if (len(self.instance_name) == 0) or (len(self.settings) == 0):
            if len(self.instance_name) + len(self.settings) != 0:
                raise self.new_exception(4077, self.instance_name, self.settings)
        if len(self.instance_name) > 0:
            self.auto_init = True
            self.initialize(self.instance_name, self.settings, self.verbose_logging)

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
        return new_szexception(
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

    @catch_ctypes_exceptions
    def add_record(
        self,
        data_source_code: str,
        record_id: str,
        record_definition: str | Dict[Any, Any],
        # TODO Is 0 correct for flags to be none? This will change when have new flag bits - works for now
        flags: int = 0,
        # TODO Code smell and pylint reports it. Investigate how to improve
        # *args: Any,
        **kwargs: Any,
    ) -> str:
        if not flags:
            result = self.library_handle.G2_addRecord(
                as_c_char_p(data_source_code),
                as_c_char_p(record_id),
                as_c_char_p(as_str(record_definition)),
            )
            if result != 0:
                raise self.new_exception(
                    4001,
                    data_source_code,
                    record_id,
                    record_definition,
                    result,
                )
            return "{}"

        result = self.library_handle.G2_addRecordWithInfo_helper(
            as_c_char_p(data_source_code),
            as_c_char_p(record_id),
            as_c_char_p(as_str(record_definition)),
            flags,
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4002,
                    data_source_code,
                    record_id,
                    record_definition,
                    flags,
                    result.return_code,
                )
            return as_python_str(result.response)

    # TODO Test @catch_ctypes_exceptions if int isn't sent
    def close_export(self, export_handle: int, *args: Any, **kwargs: Any) -> None:
        result = self.library_handle.G2_closeExport(as_uintptr_t(export_handle))
        if result != 0:
            raise self.new_exception(4006, result)

    def count_redo_records(self, *args: Any, **kwargs: Any) -> int:
        result: int = self.library_handle.G2_countRedoRecords()
        # NOTE If result >= 0 call was successful
        if result < 0:
            raise self.new_exception(4007, result)
        return result

    @catch_ctypes_exceptions
    def delete_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = 0,
        **kwargs: Any,
    ) -> str:
        if not flags:
            result = self.library_handle.G2_deleteRecord(
                as_c_char_p(data_source_code),
                as_c_char_p(record_id),
            )
            if result != 0:
                raise self.new_exception(
                    4008,
                    data_source_code,
                    record_id,
                    result,
                )
            return "{}"

        result = self.library_handle.G2_deleteRecordWithInfo_helper(
            as_c_char_p(data_source_code),
            as_c_char_p(record_id),
            flags,
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4009,
                    data_source_code,
                    record_id,
                    flags,
                    result.return_code,
                )
            return as_python_str(result.response)

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        result = self.library_handle.G2_destroy()
        if result != 0:
            raise self.new_exception(4010, result)

    @catch_ctypes_exceptions
    def export_csv_entity_report(
        self,
        # TODO add default col list and add information to abstract docstring?
        csv_column_list: str,
        flags: int = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> int:
        result = self.library_handle.G2_exportCSVEntityReport_helper(
            as_c_char_p(csv_column_list), flags
        )
        if result.return_code != 0:
            raise self.new_exception(4013, csv_column_list, flags, result.return_code)
        return as_python_int(result.export_handle)

    def export_json_entity_report(
        self,
        flags: int = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> int:
        result = self.library_handle.G2_exportJSONEntityReport_helper(flags)
        if result.return_code != 0:
            raise self.new_exception(4014, flags, result.return_code)
        return as_python_int(result.export_handle)

    def fetch_next(self, export_handle: int, *args: Any, **kwargs: Any) -> str:
        result = self.library_handle.G2_fetchNext_helper(as_uintptr_t(export_handle))
        if result.return_code != 0:
            raise self.new_exception(4015, export_handle, result.return_code)
        return as_python_str(result.response)

    # NOTE No examples of this, early adopter function and needs manual additions to Sz config to work
    # NOTE Commented out for now to discuss if worth leaving in uncommented if a customer does want to use
    # def find_interesting_entities_by_entity_id(
    #     self, entity_id: int, flags: int = 0, *args: Any, **kwargs: Any
    # ) -> str:
    #     result = self.library_handle.G2_findInterestingEntitiesByEntityID_helper(
    #         entity_id, flags
    #     )

    #     with FreeCResources(self.library_handle, result.response):
    #         if result.return_code != 0:
    #             raise self.new_exception(4016, entity_id, result.return_code)
    #         return as_python_str(result.response)

    # NOTE No examples of this, early adopter function and needs manual additions to Sz config to work
    # NOTE Commented out for now to discuss if worth leaving in uncommented if a customer does want to use
    # def find_interesting_entities_by_record_id(
    #     self,
    #     data_source_code: str,
    #     record_id: str,
    #     flags: int = 0,
    #     *args: Any,
    #     **kwargs: Any,
    # ) -> str:
    #     result = self.library_handle.G2_findInterestingEntitiesByRecordID_helper(
    #         as_c_char_p(data_source_code), as_c_char_p(record_id), flags
    #     )

    #     with FreeCResources(self.library_handle, result.response):
    #         if result.return_code != 0:
    #             raise self.new_exception(
    #                 4017, data_source_code, record_id, flags, result.return_code
    #             )
    #         return as_python_str(result.response)

    @catch_ctypes_exceptions
    def find_network_by_entity_id(
        self,
        # TODO Take entity_list as a comma separated string, tuple, other\? Others like this
        entity_list: str | Dict[Any, Any],
        max_degrees: int,
        build_out_degree: int,
        max_entities: int,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.G2_findNetworkByEntityID_V2_helper(
            as_c_char_p(as_str(entity_list)),
            max_degrees,
            build_out_degree,
            max_entities,
            flags,
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4018,
                    entity_list,
                    max_degrees,
                    build_out_degree,
                    max_entities,
                    flags,
                    result.return_code,
                )
            return as_python_str(result.response)

    @catch_ctypes_exceptions
    def find_network_by_record_id(
        self,
        record_list: str | Dict[Any, Any],
        max_degrees: int,
        build_out_degree: int,
        max_entities: int,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.G2_findNetworkByRecordID_V2_helper(
            as_c_char_p(as_str(record_list)),
            max_degrees,
            build_out_degree,
            max_entities,
            flags,
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4020,
                    record_list,
                    max_degrees,
                    build_out_degree,
                    max_entities,
                    flags,
                    result.return_code,
                )
            return as_python_str(result.response)

    # TODO Test if the logic is correct from the collapse of calls
    @catch_ctypes_exceptions
    def find_path_by_entity_id(
        self,
        start_entity_id: int,
        end_entity_id: int,
        max_degrees: int,
        # TODO Could be list of entity ids or dsrc code + record id
        exclusions: str | Dict[Any, Any] = "",
        # TODO Could be a list of codes
        required_data_sources: str | Dict[Any, Any] = "",
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> str:

        # G2_findPathByEntityID(entityID1, entityID2, maxDegree, responseBuf, bufSize, resizeFunc)
        # G2_findPathExcludingByEntityID(entityID1, entityID2, maxDegree, excludedEntities, responseBuf, bufSize, resizeFunc)
        # G2_findPathIncludingSourceByEntityID(entityID1, entityID2, maxDegree, excludedEntities, requiredDsrcs, responseBuf, bufSize, resizeFunc)

        if exclusions and not required_data_sources:
            result = self.library_handle.G2_findPathExcludingByEntityID_V2_helper(
                start_entity_id,
                end_entity_id,
                max_degrees,
                as_c_char_p(as_str(exclusions)),
                flags,
            )

            with FreeCResources(self.library_handle, result.response):
                if result.return_code != 0:
                    raise self.new_exception(
                        4027,
                        start_entity_id,
                        end_entity_id,
                        max_degrees,
                        # TODO Should this and others that could be dicts use as_str?
                        exclusions,
                        flags,
                        result.return_code,
                    )

            return as_python_str(result.response)

        if required_data_sources:
            result = self.library_handle.G2_findPathIncludingSourceByEntityID_V2_helper(
                start_entity_id,
                end_entity_id,
                max_degrees,
                as_c_char_p(as_str(exclusions)),
                as_c_char_p(as_str(required_data_sources)),
                flags,
            )

            with FreeCResources(self.library_handle, result.response):
                if result.return_code != 0:
                    raise self.new_exception(
                        4031,
                        start_entity_id,
                        end_entity_id,
                        max_degrees,
                        # TODO Should this and others that could be dicts use as_str?
                        exclusions,
                        required_data_sources,
                        flags,
                        result.return_code,
                    )

            return as_python_str(result.response)

        result = self.library_handle.G2_findPathByEntityID_V2_helper(
            start_entity_id,
            end_entity_id,
            max_degrees,
            flags,
        )
        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4023,
                    start_entity_id,
                    end_entity_id,
                    max_degrees,
                    flags,
                    result.return_code,
                )
            return as_python_str(result.response)

    # TODO Test if the logic is correct from the collapse of calls
    @catch_ctypes_exceptions
    def find_path_by_record_id(
        self,
        start_data_source_code: str,
        start_record_id: str,
        end_data_source_code: str,
        end_record_id: str,
        max_degrees: int,
        exclusions: str | Dict[Any, Any] = "",
        required_data_sources: str | Dict[Any, Any] = "",
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> str:

        if exclusions and not required_data_sources:
            result = self.library_handle.G2_findPathExcludingByRecordID_V2_helper(
                as_c_char_p(start_data_source_code),
                as_c_char_p(start_record_id),
                as_c_char_p(end_data_source_code),
                as_c_char_p(end_record_id),
                max_degrees,
                as_c_char_p(as_str(exclusions)),
                flags,
            )

            with FreeCResources(self.library_handle, result.response):
                if result.return_code != 0:
                    raise self.new_exception(
                        4029,
                        start_data_source_code,
                        start_record_id,
                        end_data_source_code,
                        end_record_id,
                        max_degrees,
                        exclusions,
                        flags,
                        result.return_code,
                    )
                return as_python_str(result.response)

        if required_data_sources:
            result = self.library_handle.G2_findPathIncludingSourceByRecordID_V2_helper(
                as_c_char_p(start_data_source_code),
                as_c_char_p(start_record_id),
                as_c_char_p(end_data_source_code),
                as_c_char_p(end_record_id),
                max_degrees,
                as_c_char_p(as_str(exclusions)),
                as_c_char_p(as_str(required_data_sources)),
                flags,
            )

            with FreeCResources(self.library_handle, result.response):
                if result.return_code != 0:
                    raise self.new_exception(
                        4031,
                        start_data_source_code,
                        start_record_id,
                        end_data_source_code,
                        end_record_id,
                        max_degrees,
                        exclusions,
                        required_data_sources,
                        flags,
                        result.return_code,
                    )
                return as_python_str(result.response)

        result = self.library_handle.G2_findPathByRecordID_V2_helper(
            as_c_char_p(start_data_source_code),
            as_c_char_p(start_record_id),
            as_c_char_p(end_data_source_code),
            as_c_char_p(end_record_id),
            max_degrees,
            flags,
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4025,
                    start_data_source_code,
                    start_record_id,
                    end_data_source_code,
                    end_record_id,
                    max_degrees,
                    flags,
                    result.return_code,
                )
            return as_python_str(result.response)

    def get_active_config_id(self, *args: Any, **kwargs: Any) -> int:
        result = self.library_handle.G2_getActiveConfigID_helper()
        if result.return_code != 0:
            raise self.new_exception(4034, result.return_code)
        return as_python_int(result.response)

    def get_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.G2_getEntityByEntityID_V2_helper(entity_id, flags)

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(4035, entity_id, flags, result.return_code)
            return as_python_str(result.response)

    @catch_ctypes_exceptions
    def get_entity_by_record_id(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.G2_getEntityByRecordID_V2_helper(
            as_c_char_p(data_source_code), as_c_char_p(record_id), flags
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4037, data_source_code, record_id, result.return_code
                )
            return as_python_str(result.response)

    @catch_ctypes_exceptions
    def get_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.G2_getRecord_V2_helper(
            as_c_char_p(data_source_code),
            as_c_char_p(record_id),
            flags,
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4040,
                    data_source_code,
                    record_id,
                    flags,
                    result.return_code,
                )
            return as_python_str(result.response)

    def get_redo_record(self, *args: Any, **kwargs: Any) -> str:
        result = self.library_handle.G2_getRedoRecord_helper()

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(4042, result.return_code)
            return as_python_str(result.response)

    def get_repository_last_modified_time(self, *args: Any, **kwargs: Any) -> int:
        result = self.library_handle.G2_getRepositoryLastModifiedTime_helper()
        if result.return_code != 0:
            raise self.new_exception(4043, result.return_code)
        return int(result.time)

    def get_stats(self, *args: Any, **kwargs: Any) -> str:
        result = self.library_handle.G2_stats_helper()

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(4067, result.return_code)
            return as_python_str(result.response)

    @catch_ctypes_exceptions
    def get_virtual_entity_by_record_id(
        self,
        record_list: str | Dict[Any, Any],
        flags: int = SzEngineFlags.SZ_VIRTUAL_ENTITY_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.G2_getVirtualEntityByRecordID_V2_helper(
            as_c_char_p(as_str(record_list)), flags
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(4044, record_list, result.return_code)
            return as_python_str(result.response)

    def how_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_HOW_ENTITY_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.G2_howEntityByEntityID_V2_helper(entity_id, flags)

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(4046, flags, result.return_code)
            return as_python_str(result.response)

    @catch_ctypes_exceptions
    def initialize(
        self,
        instance_name: str,
        settings: str | Dict[Any, Any],
        verbose_logging: int = 0,
        config_id: Optional[int] = None,
        **kwargs: Any,
    ) -> None:

        if not config_id:
            result = self.library_handle.G2_init(
                as_c_char_p(instance_name),
                as_c_char_p(as_str(settings)),
                verbose_logging,
            )
            if result < 0:
                raise self.new_exception(
                    4048, instance_name, settings, verbose_logging, result
                )
            return

        result = self.library_handle.G2_initWithConfigID(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            config_id,
            verbose_logging,
        )
        if result < 0:
            raise self.new_exception(
                4049,
                instance_name,
                settings,
                verbose_logging,
                config_id,
                result,
            )

    def prime_engine(self, *args: Any, **kwargs: Any) -> None:
        result = self.library_handle.G2_primeEngine()
        if result < 0:
            raise self.new_exception(4050, result)

    @catch_ctypes_exceptions
    def process_redo_record(
        self, redo_record: str, flags: int = 0, **kwargs: Any
    ) -> str:
        if not flags:
            result = self.library_handle.G2_processRedoRecord(
                as_c_char_p(redo_record),
            )
            if result != 0:
                raise self.new_exception(
                    4052,
                    result,
                )
            return "{}"

        result = self.library_handle.G2_processRedoRecordWithInfo_helper(
            as_c_char_p(redo_record),
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4053,
                    flags,
                    result.return_code,
                )
            return as_python_str(result.response)

    def reevaluate_entity(
        self, entity_id: int, flags: int = 0, *args: Any, **kwargs: Any
    ) -> str:
        if not flags:
            result = self.library_handle.G2_reevaluateEntity(entity_id, flags)
            if result < 0:
                raise self.new_exception(4058, result)
            return "{}"

        result = self.library_handle.G2_reevaluateEntityWithInfo_helper(
            entity_id,
            flags,
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4059,
                    entity_id,
                    flags,
                    # 0,
                    result.return_code,
                )
            return as_python_str(result.response)

    # TODO Test when get new build with_info, on unfixed merge build with_info returns nothing if the record_id
    # TODO doesn't exist but raises error if the dsrc_code doesn't exist
    # TODO GDEV-3790
    @catch_ctypes_exceptions
    def reevaluate_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        if not flags:
            result = self.library_handle.G2_reevaluateRecord(
                as_c_char_p(data_source_code), as_c_char_p(record_id), flags
            )
            if result < 0:
                print(f"{result = }")
                raise self.new_exception(
                    4060, data_source_code, record_id, flags, result
                )
            return "{}"

        result = self.library_handle.G2_reevaluateRecordWithInfo_helper(
            as_c_char_p(data_source_code),
            as_c_char_p(record_id),
            flags,
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4061,
                    data_source_code,
                    record_id,
                    flags,
                    result.return_code,
                )
            return as_python_str(result.response)

    def reinitialize(self, config_id: int, *args: Any, **kwargs: Any) -> None:
        result = self.library_handle.G2_reinit(config_id)
        if result < 0:
            raise self.new_exception(4062, config_id, result)

    @catch_ctypes_exceptions
    def replace_record(
        self,
        data_source_code: str,
        record_id: str,
        record_definition: str | Dict[Any, Any],
        flags: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        if not flags:
            result = self.library_handle.G2_replaceRecord(
                as_c_char_p(data_source_code),
                as_c_char_p(record_id),
                as_c_char_p(as_str(record_definition)),
            )
            if result != 0:
                raise self.new_exception(
                    4063, data_source_code, record_id, record_definition, result
                )
            return "{}"

        result = self.library_handle.G2_replaceRecordWithInfo_helper(
            as_c_char_p(data_source_code),
            as_c_char_p(record_id),
            as_c_char_p(as_str(record_definition)),
            flags,
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4002,
                    data_source_code,
                    record_id,
                    record_definition,
                    flags,
                    result.return_code,
                )
            return as_python_str(result.response)

    @catch_ctypes_exceptions
    def search_by_attributes(
        self,
        attributes: str | Dict[Any, Any],
        search_profile: str = "SEARCH",
        flags: int = SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.G2_searchByAttributes_V3_helper(
            as_c_char_p(as_str(attributes)),
            as_c_char_p(as_str(search_profile)),
            flags,
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                # TODO 4077 needs to be reordered in engine_abstract
                raise self.new_exception(
                    4077,
                    attributes,
                    search_profile,
                    flags,
                    result.return_code,
                )
            return as_python_str(result.response)

    @catch_ctypes_exceptions
    def why_entities(
        self,
        entity_id_1: int,
        entity_id_2: int,
        flags: int = SzEngineFlags.SZ_WHY_ENTITIES_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.G2_whyEntities_V2_helper(
            entity_id_1,
            entity_id_2,
            flags,
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4068, entity_id_1, entity_id_2, result.return_code
                )
            return as_python_str(result.response)

    @catch_ctypes_exceptions
    def why_records(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        flags: int = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.G2_whyRecords_V2_helper(
            as_c_char_p(data_source_code_1),
            as_c_char_p(record_id_1),
            as_c_char_p(data_source_code_2),
            as_c_char_p(record_id_2),
            flags,
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4074,
                    data_source_code_1,
                    record_id_1,
                    data_source_code_2,
                    record_id_2,
                    flags,
                    result.return_code,
                )
            return as_python_str(result.response)

    @catch_ctypes_exceptions
    def why_record_in_entity(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.G2_whyRecordInEntity_V2_helper(
            as_c_char_p(data_source_code),
            as_c_char_p(record_id),
            flags,
        )

        with FreeCResources(self.library_handle, result.response):
            if result.return_code != 0:
                raise self.new_exception(
                    4078,
                    data_source_code,
                    record_id,
                    flags,
                    result.return_code,
                )
            return as_python_str(result.response)
