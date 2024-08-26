"""
The szengine package is used to insert, update, delete and query records and entities in the Senzing product.
It is a wrapper over Senzing's SzEngine C binding.
It conforms to the interface specified in
`szengine_abstract.py <https://github.com/senzing-garage/sz-sdk-python/blob/main/src/senzing_abstract/szengine_abstract.py>`_

# TODO: LD_LIBRARY_PATH is only for Linux
To use szengine,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/g2/lib
"""

# pylint: disable=R0903,C0302,R0915
# NOTE Used for ctypes type hinting - https://stackoverflow.com/questions/77619149/python-ctypes-pointer-type-hinting
from __future__ import annotations

import sys

# TODO - Ant -
from ctypes import (
    POINTER,
    Structure,
    c_char,
    c_char_p,
    c_int,
    c_longlong,
    c_uint,
    c_void_p,
    create_string_buffer,
)
from functools import partial
from typing import Any, Dict, List, Optional, Tuple, Union

from senzing import SzEngineAbstract, SzEngineFlags

from ._helpers import (
    FreeCResources,
    as_c_char_p,
    as_c_uintptr_t,
    as_python_str,
    as_str,
    build_data_sources_json,
    build_entities_json,
    build_records_json,
    catch_exceptions,
    check_result_rc,
    load_sz_library,
    sdk_exception,
)
from ._version import is_supported_senzingapi_version

# Metadata

__all__ = ["SzEngine"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-15"

# SENZING_PRODUCT_ID = "5043"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md

# -----------------------------------------------------------------------------
# Classes that are result structures from calls to Senzing
# -----------------------------------------------------------------------------


class SzResponseReturnCodeResult(Structure):
    """Simple response, return_code structure"""

    _fields_ = [
        ("response", POINTER(c_char)),
        ("return_code", c_longlong),
    ]


class SzResponseLonglongReturnCodeResult(Structure):
    """Simple response, return_code structure"""

    _fields_ = [
        ("response", c_longlong),
        ("return_code", c_longlong),
    ]


class SzAddRecordWithInfoResult(SzResponseReturnCodeResult):
    # TODO - Ant - correct golang_helpers.h and check other modules
    """In golang_helpers.h Sz_addRecordWithInfo_result"""


class SzDeleteRecordWithInfoResult(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_deleteRecordWithInfo_result"""


class SzExportCSVEntityReportResult(Structure):
    """In golang_helpers.h Sz_exportCSVEntityReport_result"""

    _fields_ = [
        ("export_handle", c_void_p),
        ("return_code", c_longlong),
    ]


class SzExportJSONEntityReportResult(Structure):
    """In golang_helpers.h Sz_exportJSONEntityReport_result"""

    _fields_ = [
        ("export_handle", c_void_p),
        ("return_code", c_longlong),
    ]


class SzFetchNextResult(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_fetchNext_result"""


class SzFindInterestingEntitiesByEntityIDResult(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_findInterestingEntitiesByEntityID_result"""


class SzFindInterestingEntitiesByRecordIDResult(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_findInterestingEntitiesByRecordID_result"""


class SzFindNetworkByEntityIDV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_findNetworkByEntityID_V2_result"""


class SzFindNetworkByRecordIDV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_findNetworkByRecordID_V2_result"""


class SzFindPathByEntityIDV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_findPathByEntityID_V2_result"""


class SzFindPathByRecordIDV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_findPathByRecordID_V2_result"""


class SzFindPathExcludingByEntityIDV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_findPathExcludingByEntityID_V2_result"""


class SzFindPathExcludingByRecordIDV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_findPathExcludingByRecordID_V2_result"""


class SzFindPathIncludingSourceByEntityIDV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_findPathIncludingSourceByEntityID_V2_result"""


class SzFindPathIncludingSourceByRecordIDV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_findPathIncludingSourceByRecordID_V2_result"""


class SzGetActiveConfigIDResult(SzResponseLonglongReturnCodeResult):
    """In golang_helpers.h Sz_getActiveConfigID_result"""


class SzGetEntityByEntityIDV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_getEntityByEntityID_V2_result"""


class SzGetEntityByRecordIDV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_getEntityByRecordID_V2_result"""


class SzGetRecordV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_getRecord_V2_result"""


class SzGetRedoRecordResult(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_getRedoRecord_result"""


class SzGetVirtualEntityByRecordIDV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_getVirtualEntityByRecordID_V2_result"""


class SzHowEntityByEntityIDV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_howEntityByEntityID_V2_result"""


class SzProcessRedoRecordWithInfoResult(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_processRedoRecordWithInfo_result"""


class SzReevaluateEntityWithInfoResult(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_reevaluateEntityWithInfo_result"""


class SzReevaluateRecordWithInfoResult(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_reevaluateRecordWithInfo_result"""


class SzSearchByAttributesV3Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_searchByAttributes_V2_result"""


class SzStatsResult(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_stats_result"""


class SzWhyEntitiesV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_whyEntities_V2_result"""


class SzWhyRecordInEntityV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_whyRecordInEntity_V2_result"""


class SzWhyRecordsV2Result(SzResponseReturnCodeResult):
    """In golang_helpers.h Sz_whyRecords_V2_result"""


# -----------------------------------------------------------------------------
# SzEngine class
# -----------------------------------------------------------------------------


class SzEngine(SzEngineAbstract):
    """
    The `initialize` method initializes the Senzing SzEngine object.
    It must be called prior to any other calls.

    **Note:** If the SzEngine constructor is called with parameters,
    the constructor will automatically call the `initialize()` method.

    Example:

    .. code-block:: python

        sz_engine = SzEngine(instance_name, settings)


    If the SzEngine constructor is called without parameters,
    the `initialize()` method must be called to initialize the use of SzEngine.

    Example:

    .. code-block:: python

        sz_engine = SzEngine()
        sz_engine.initialize(instance_name, settings, verbose_logging)

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
        SzError: Failed to load the Senzing library or incorrect `instance_name`, `settings` combination.

    .. collapse:: Example:

        .. literalinclude:: ../../examples/szengine/szengine_constructor.py
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

        # Mask for removing SDK specific flags not supplied to method call
        self.sdk_flags_mask = ~(SzEngineFlags.SZ_WITH_INFO)

        # Empty response for methods where with info can optionally be
        # returned but was not requested
        self.no_info = "{}"

        # Determine if Senzing API version is acceptable.
        is_supported_senzingapi_version()

        # Load binary library.
        self.library_handle = load_sz_library()

        # Partial function to use this modules self.library_handle for exception handling
        self.check_result = partial(
            check_result_rc,
            self.library_handle.Sz_getLastException,
            self.library_handle.Sz_clearLastException,
            self.library_handle.Sz_getLastExceptionCode,
        )

        # Initialize C function input parameters and results.
        # Must be synchronized with g2/sdk/c/libg2engine.h

        self.library_handle.Sz_addRecord.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
        ]
        self.library_handle.Sz_addRecord.restype = c_longlong
        self.library_handle.Sz_addRecordWithInfo_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_addRecordWithInfo_helper.restype = (
            SzAddRecordWithInfoResult
        )
        self.library_handle.Sz_closeExport_helper.argtypes = [
            POINTER(c_uint),
        ]
        self.library_handle.Sz_closeExport_helper.restype = c_longlong
        self.library_handle.Sz_countRedoRecords.argtypes = []
        self.library_handle.Sz_countRedoRecords.restype = c_longlong
        self.library_handle.Sz_deleteRecord.argtypes = [
            c_char_p,
            c_char_p,
        ]
        self.library_handle.Sz_deleteRecord.restype = c_longlong
        self.library_handle.Sz_deleteRecordWithInfo_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_deleteRecordWithInfo_helper.restype = (
            SzDeleteRecordWithInfoResult
        )
        self.library_handle.Sz_destroy.argtypes = []
        self.library_handle.Sz_destroy.restype = c_longlong
        self.library_handle.Sz_exportCSVEntityReport_helper.argtypes = [
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_exportCSVEntityReport_helper.restype = (
            SzExportCSVEntityReportResult
        )
        self.library_handle.Sz_exportJSONEntityReport_helper.argtypes = [c_longlong]
        self.library_handle.Sz_exportJSONEntityReport_helper.restype = (
            SzExportJSONEntityReportResult
        )
        self.library_handle.Sz_fetchNext_helper.argtypes = [
            POINTER(c_uint),
        ]
        self.library_handle.Sz_fetchNext_helper.restype = SzFetchNextResult
        self.library_handle.Sz_findInterestingEntitiesByEntityID_helper.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self.library_handle.Sz_findInterestingEntitiesByEntityID_helper.restype = (
            SzFindInterestingEntitiesByEntityIDResult
        )
        self.library_handle.Sz_findInterestingEntitiesByRecordID_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_findInterestingEntitiesByRecordID_helper.restype = (
            SzFindInterestingEntitiesByRecordIDResult
        )
        self.library_handle.Sz_findNetworkByEntityID_V2_helper.argtypes = [
            c_char_p,
            c_longlong,
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.Sz_findNetworkByEntityID_V2_helper.restype = (
            SzFindNetworkByEntityIDV2Result
        )
        self.library_handle.Sz_findNetworkByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_longlong,
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.Sz_findNetworkByRecordID_V2_helper.restype = (
            SzFindNetworkByRecordIDV2Result
        )
        self.library_handle.Sz_findPathByEntityID_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.Sz_findPathByEntityID_V2_helper.restype = (
            SzFindPathByEntityIDV2Result
        )
        self.library_handle.Sz_findPathByEntityIDIncludingSource_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_findPathByEntityIDIncludingSource_V2_helper.restype = (
            SzFindPathIncludingSourceByEntityIDV2Result
        )
        self.library_handle.Sz_findPathByEntityIDWithAvoids_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_findPathByEntityIDWithAvoids_V2_helper.restype = (
            SzFindPathExcludingByEntityIDV2Result
        )
        self.library_handle.Sz_findPathByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.Sz_findPathByRecordID_V2_helper.restype = (
            SzFindPathByRecordIDV2Result
        )
        self.library_handle.Sz_findPathByRecordIDIncludingSource_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_findPathByRecordIDIncludingSource_V2_helper.restype = (
            SzFindPathIncludingSourceByRecordIDV2Result
        )
        self.library_handle.Sz_findPathByRecordIDWithAvoids_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_findPathByRecordIDWithAvoids_V2_helper.restype = (
            SzFindPathExcludingByRecordIDV2Result
        )
        self.library_handle.Sz_getActiveConfigID_helper.argtypes = []
        self.library_handle.Sz_getActiveConfigID_helper.restype = (
            SzGetActiveConfigIDResult
        )
        self.library_handle.Sz_getEntityByEntityID_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self.library_handle.Sz_getEntityByEntityID_V2_helper.restype = (
            SzGetEntityByEntityIDV2Result
        )
        self.library_handle.Sz_getEntityByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_getEntityByRecordID_V2_helper.restype = (
            SzGetEntityByRecordIDV2Result
        )
        self.library_handle.Sz_getRecord_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_getRecord_V2_helper.restype = SzGetRecordV2Result
        self.library_handle.Sz_getRedoRecord_helper.argtypes = []
        self.library_handle.Sz_getRedoRecord_helper.restype = SzGetRedoRecordResult
        self.library_handle.Sz_getVirtualEntityByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_getVirtualEntityByRecordID_V2_helper.restype = (
            SzGetVirtualEntityByRecordIDV2Result
        )
        self.library_handle.Sz_howEntityByEntityID_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self.library_handle.Sz_howEntityByEntityID_V2_helper.restype = (
            SzHowEntityByEntityIDV2Result
        )
        self.library_handle.Sz_init.argtypes = [c_char_p, c_char_p, c_int]
        self.library_handle.Sz_init.restype = c_longlong
        self.library_handle.Sz_initWithConfigID.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.Sz_processRedoRecord.argtypes = [
            c_char_p,
        ]
        self.library_handle.Sz_processRedoRecord.restype = c_longlong
        self.library_handle.Sz_processRedoRecordWithInfo_helper.argtypes = [
            c_char_p,
        ]
        self.library_handle.Sz_processRedoRecordWithInfo_helper.restype = (
            SzProcessRedoRecordWithInfoResult
        )
        self.library_handle.Sz_reevaluateEntity.argtypes = [c_longlong, c_longlong]
        self.library_handle.Sz_reevaluateEntity.restype = c_longlong
        self.library_handle.Sz_reevaluateEntityWithInfo_helper.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self.library_handle.Sz_reevaluateEntityWithInfo_helper.restype = (
            SzReevaluateEntityWithInfoResult
        )
        self.library_handle.Sz_reevaluateRecord.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_reevaluateRecord.restype = c_longlong
        self.library_handle.Sz_reevaluateRecordWithInfo_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_reevaluateRecordWithInfo_helper.restype = (
            SzReevaluateRecordWithInfoResult
        )
        self.library_handle.Sz_reinit.argtypes = [c_longlong]
        self.library_handle.Sz_reinit.restype = c_longlong
        self.library_handle.Sz_searchByAttributes_V3_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_searchByAttributes_V3_helper.restype = (
            SzSearchByAttributesV3Result
        )
        self.library_handle.Sz_stats_helper.argtypes = []
        self.library_handle.Sz_stats_helper.restype = SzStatsResult
        self.library_handle.Sz_whyEntities_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self.library_handle.Sz_whyEntities_V2_helper.restype = SzWhyEntitiesV2Result
        self.library_handle.Sz_whyRecordInEntity_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_whyRecordInEntity_V2_helper.restype = (
            SzWhyRecordInEntityV2Result
        )
        self.library_handle.Sz_whyRecords_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self.library_handle.Sz_whyRecords_V2_helper.restype = SzWhyRecordsV2Result
        self.library_handle.SzHelper_free.argtypes = [c_char_p]

        if not self.instance_name or len(self.settings) == 0:
            raise sdk_exception(2)

        # TODO - Ant -
        print(
            f"\tszengine.__init__() before calling _initialize: \n\t\t{self.initialized = } \n\t\t{self.library_handle = }\n\t\t{sys.getrefcount(self) - 1 = }",
            flush=True,
        )
        # input("\nPress a key to complete...")

        # Initialize Senzing engine.
        self._initialize(
            instance_name=self.instance_name,
            settings=self.settings,
            config_id=self.config_id,
            verbose_logging=self.verbose_logging,
        )
        self.initialized = True

        # TODO - Ant -
        print(
            f"\tszengine.__init__() after calling _initialize: \n\t\t{self.initialized = } \n\t\t{self.library_handle = }\n\t\t{sys.getrefcount(self) - 1 = }",
            flush=True,
        )
        print(f"\t\t{id(self) = }", flush=True)
        # input("\nPress a key to complete...")

        # # TODO - Ant -
        # weakref.finalize(self, self._destroy)

    def __del__(self) -> None:
        """Destructor"""
        # TODO - Ant -
        print(
            f"\tszengine.__del__(): \n\t\t{self.initialized = } \n\t\t{self.library_handle = }",
            flush=True,
        )
        # # if self.initialized:
        # # with suppress(Exception):
        # self._destroy()

        # if self.initialized:
        # with suppress(Exception):
        self._destroy()

    # -------------------------------------------------------------------------
    # SzEngine methods
    # -------------------------------------------------------------------------

    # TODO - Ant - Macy method, needed in final?
    @catch_exceptions
    def bulk_load(
        self,
        records: List[str],
        # flags: int = 0,
        **kwargs: Any,
    ) -> str:
        """Internal method"""

        try:
            c_records = (POINTER(c_char) * (len(records) + 1))()

            i = 0
            for rec in records:
                c_records[i] = create_string_buffer(rec.encode())  # type: ignore[call-overload]
                i += 1
            c_records[len(records)] = None  # type: ignore[call-overload]

            result = self.library_handle.Szinternal_bulkLoad(c_records)
            self.check_result(result)
        except Exception as err:
            print(err)
            raise

        return self.no_info

    @catch_exceptions
    def add_record(
        self,
        data_source_code: str,
        record_id: str,
        record_definition: str,
        flags: int = 0,
        **kwargs: Any,
    ) -> str:
        if (flags & SzEngineFlags.SZ_WITH_INFO) != 0:
            base_flags = flags & self.sdk_flags_mask
            result = self.library_handle.Sz_addRecordWithInfo_helper(
                as_c_char_p(data_source_code),
                as_c_char_p(record_id),
                as_c_char_p(record_definition),
                base_flags,
            )
            with FreeCResources(self.library_handle, result.response):
                self.check_result(result.return_code)
                return as_python_str(result.response)

        result = self.library_handle.Sz_addRecord(
            as_c_char_p(data_source_code),
            as_c_char_p(record_id),
            as_c_char_p(record_definition),
        )
        self.check_result(result)
        return self.no_info

    @catch_exceptions
    def close_export(self, export_handle: int, **kwargs: Any) -> None:
        result = self.library_handle.Sz_closeExport_helper(
            as_c_uintptr_t(export_handle)
        )
        self.check_result(result)

    def count_redo_records(self, **kwargs: Any) -> int:
        result: int = self.library_handle.Sz_countRedoRecords()
        if result < 0:
            self.check_result(result)
        return result

    @catch_exceptions
    def delete_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = 0,
        **kwargs: Any,
    ) -> str:
        if (flags & SzEngineFlags.SZ_WITH_INFO) != 0:
            base_flags = flags & self.sdk_flags_mask
            result = self.library_handle.Sz_deleteRecordWithInfo_helper(
                as_c_char_p(data_source_code),
                as_c_char_p(record_id),
                base_flags,
            )
            with FreeCResources(self.library_handle, result.response):
                self.check_result(result.return_code)
                return as_python_str(result.response)

        result = self.library_handle.Sz_deleteRecord(
            as_c_char_p(data_source_code),
            as_c_char_p(record_id),
        )
        self.check_result(result)
        return self.no_info

    # TODO - Ant - @catch_exceptions or don't care?
    def _destroy(self, **kwargs: Any) -> None:
        # TODO - Ant -
        print(
            f"\tszengine._destroy(): \n\t\t{self.library_handle = }\n\t\t{self.initialized = }\n\t\t{id(self) = }\n\t\t{sys.getrefcount(self) - 1 = }",
            flush=True,
        )
        # _ = self.library_handle.Sz_destroy()
        # TODO - Ant -
        if self.initialized:
            _ = self.library_handle.Sz_destroy()
            # print(f"\tBack from Sz_destroy(): \n\t\t{r = }", flush=True)
            # print("\nCollecting garbage")
            # gc.collect()
            self.initialized = False
        else:
            print("\t\tNot destroying, not initialized...", flush=True)
        # print(f"\n{gc.get_objects() = }")

    # # TODO - Ant - @catch_exceptions or don't care?
    # def _destroy(self, **kwargs: Any) -> None:
    #     # TODO - Ant -
    #     print(
    #         f"\tszengine._destroy(): \n\t\t{self.library_handle = }\n\t\t{self.initialized = }\n\t\t{id(self) = }\n\t\t{sys.getrefcount(self) - 1 = }",
    #         flush=True,
    #     )
    #     _ = self.library_handle.Sz_destroy()

    @catch_exceptions
    def export_csv_entity_report(
        self,
        csv_column_list: str,
        flags: int = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> int:
        result = self.library_handle.Sz_exportCSVEntityReport_helper(
            as_c_char_p(csv_column_list), flags
        )
        self.check_result(result.return_code)
        return result.export_handle  # type: ignore[no-any-return]

    def export_json_entity_report(
        self,
        flags: int = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> int:
        result = self.library_handle.Sz_exportJSONEntityReport_helper(flags)
        self.check_result(result.return_code)
        return result.export_handle  # type: ignore[no-any-return]

    @catch_exceptions
    def fetch_next(self, export_handle: int, **kwargs: Any) -> str:
        result = self.library_handle.Sz_fetchNext_helper(as_c_uintptr_t(export_handle))
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    # NOTE Included but not documented or examples, early adaptor feature, needs manual additions to config
    def find_interesting_entities_by_entity_id(
        self, entity_id: int, flags: int = 0, **kwargs: Any
    ) -> str:
        result = self.library_handle.Sz_findInterestingEntitiesByEntityID_helper(
            entity_id, flags
        )
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    # NOTE Included but not documented or examples, early adaptor feature, needs manual additions to config
    def find_interesting_entities_by_record_id(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = 0,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.Sz_findInterestingEntitiesByRecordID_helper(
            as_c_char_p(data_source_code), as_c_char_p(record_id), flags
        )
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    @catch_exceptions
    def find_network_by_entity_id(
        self,
        entity_ids: List[int],
        max_degrees: int,
        build_out_degree: int,
        build_out_max_entities: int,
        flags: int = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.Sz_findNetworkByEntityID_V2_helper(
            as_c_char_p(build_entities_json(entity_ids)),
            max_degrees,
            build_out_degree,
            build_out_max_entities,
            flags,
        )

        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    @catch_exceptions
    def find_network_by_record_id(
        self,
        record_keys: List[Tuple[str, str]],
        max_degrees: int,
        build_out_degree: int,
        build_out_max_entities: int,
        flags: int = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.Sz_findNetworkByRecordID_V2_helper(
            as_c_char_p(build_records_json(record_keys)),
            max_degrees,
            build_out_degree,
            build_out_max_entities,
            flags,
        )
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    # TODO Needs additional tests with combination of optional args
    @catch_exceptions
    def find_path_by_entity_id(
        self,
        start_entity_id: int,
        end_entity_id: int,
        max_degrees: int,
        avoid_entity_ids: Optional[List[int]] = None,
        required_data_sources: Optional[List[str]] = None,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        if avoid_entity_ids and not required_data_sources:
            result = self.library_handle.Sz_findPathByEntityIDWithAvoids_V2_helper(
                start_entity_id,
                end_entity_id,
                max_degrees,
                as_c_char_p(build_entities_json(avoid_entity_ids)),
                flags,
            )
        elif required_data_sources:
            result = self.library_handle.Sz_findPathByEntityIDIncludingSource_V2_helper(
                start_entity_id,
                end_entity_id,
                max_degrees,
                as_c_char_p(build_entities_json(avoid_entity_ids)),
                as_c_char_p(build_data_sources_json(required_data_sources)),
                flags,
            )
        else:
            result = self.library_handle.Sz_findPathByEntityID_V2_helper(
                start_entity_id,
                end_entity_id,
                max_degrees,
                flags,
            )
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    # TODO Needs additional tests with combination of optional args
    @catch_exceptions
    def find_path_by_record_id(
        self,
        start_data_source_code: str,
        start_record_id: str,
        end_data_source_code: str,
        end_record_id: str,
        max_degrees: int,
        avoid_record_keys: Optional[List[Tuple[str, str]]] = None,
        required_data_sources: Optional[List[str]] = None,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        if avoid_record_keys and not required_data_sources:
            result = self.library_handle.Sz_findPathByRecordIDWithAvoids_V2_helper(
                as_c_char_p(start_data_source_code),
                as_c_char_p(start_record_id),
                as_c_char_p(end_data_source_code),
                as_c_char_p(end_record_id),
                max_degrees,
                as_c_char_p(build_records_json(avoid_record_keys)),
                flags,
            )
        elif required_data_sources:
            result = self.library_handle.Sz_findPathByRecordIDIncludingSource_V2_helper(
                as_c_char_p(start_data_source_code),
                as_c_char_p(start_record_id),
                as_c_char_p(end_data_source_code),
                as_c_char_p(end_record_id),
                max_degrees,
                as_c_char_p(build_records_json(avoid_record_keys)),
                as_c_char_p(build_data_sources_json(required_data_sources)),
                flags,
            )
        else:
            result = self.library_handle.Sz_findPathByRecordID_V2_helper(
                as_c_char_p(start_data_source_code),
                as_c_char_p(start_record_id),
                as_c_char_p(end_data_source_code),
                as_c_char_p(end_record_id),
                max_degrees,
                flags,
            )
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    def get_active_config_id(self, **kwargs: Any) -> int:
        result = self.library_handle.Sz_getActiveConfigID_helper()
        self.check_result(result.return_code)
        return result.response  # type: ignore[no-any-return]

    def get_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.Sz_getEntityByEntityID_V2_helper(entity_id, flags)
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    @catch_exceptions
    def get_entity_by_record_id(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.Sz_getEntityByRecordID_V2_helper(
            as_c_char_p(data_source_code), as_c_char_p(record_id), flags
        )
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    @catch_exceptions
    def get_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.Sz_getRecord_V2_helper(
            as_c_char_p(data_source_code),
            as_c_char_p(record_id),
            flags,
        )
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    def get_redo_record(self, **kwargs: Any) -> str:
        result = self.library_handle.Sz_getRedoRecord_helper()
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    def get_stats(self, **kwargs: Any) -> str:
        result = self.library_handle.Sz_stats_helper()
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    @catch_exceptions
    def get_virtual_entity_by_record_id(
        self,
        record_keys: List[Tuple[str, str]],
        flags: int = SzEngineFlags.SZ_VIRTUAL_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.Sz_getVirtualEntityByRecordID_V2_helper(
            as_c_char_p(build_records_json(record_keys)),
            flags,
        )
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    def how_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_HOW_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.Sz_howEntityByEntityID_V2_helper(entity_id, flags)
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
            result = self.library_handle.Sz_init(
                as_c_char_p(instance_name),
                as_c_char_p(as_str(settings)),
                verbose_logging,
            )
            self.check_result(result)
            return

        result = self.library_handle.Sz_initWithConfigID(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            config_id,
            verbose_logging,
        )
        self.check_result(result)

    # TODO - Ant - @catch_exceptions?
    def prime_engine(self, **kwargs: Any) -> None:
        result = self.library_handle.Sz_primeEngine()
        self.check_result(result)

    @catch_exceptions
    def process_redo_record(
        self, redo_record: str, flags: int = 0, **kwargs: Any
    ) -> str:
        if (flags & SzEngineFlags.SZ_WITH_INFO) != 0:
            base_flags = flags & self.sdk_flags_mask
            result = self.library_handle.Sz_processRedoRecordWithInfo_helper(
                as_c_char_p(redo_record), base_flags
            )
            with FreeCResources(self.library_handle, result.response):
                self.check_result(result.return_code)
                return as_python_str(result.response)

        result = self.library_handle.Sz_processRedoRecord(
            as_c_char_p(redo_record),
        )
        self.check_result(result)
        return self.no_info

    def reevaluate_entity(self, entity_id: int, flags: int = 0, **kwargs: Any) -> str:
        if (flags & SzEngineFlags.SZ_WITH_INFO) != 0:
            base_flags = flags & self.sdk_flags_mask
            result = self.library_handle.Sz_reevaluateEntityWithInfo_helper(
                entity_id,
                base_flags,
            )
            with FreeCResources(self.library_handle, result.response):
                self.check_result(result.return_code)
                response_str = as_python_str(result.response)
                return response_str if response_str else self.no_info

        result = self.library_handle.Sz_reevaluateEntity(entity_id, flags)
        self.check_result(result)
        return self.no_info

    @catch_exceptions
    def reevaluate_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = 0,
        **kwargs: Any,
    ) -> str:
        if (flags & SzEngineFlags.SZ_WITH_INFO) != 0:
            base_flags = flags & self.sdk_flags_mask
            result = self.library_handle.Sz_reevaluateRecordWithInfo_helper(
                as_c_char_p(data_source_code),
                as_c_char_p(record_id),
                base_flags,
            )
            with FreeCResources(self.library_handle, result.response):
                self.check_result(result.return_code)
                response_str = as_python_str(result.response)
                return response_str if response_str else self.no_info

        result = self.library_handle.Sz_reevaluateRecord(
            as_c_char_p(data_source_code), as_c_char_p(record_id), flags
        )
        self.check_result(result)
        return self.no_info

    def reinitialize(self, config_id: int, **kwargs: Any) -> None:
        result = self.library_handle.Sz_reinit(config_id)
        self.check_result(result)

    @catch_exceptions
    def search_by_attributes(
        self,
        attributes: str,
        flags: int = SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS,
        search_profile: str = "",
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.Sz_searchByAttributes_V3_helper(
            as_c_char_p(attributes),
            as_c_char_p(search_profile),
            flags,
        )
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    @catch_exceptions
    def why_entities(
        self,
        entity_id_1: int,
        entity_id_2: int,
        flags: int = SzEngineFlags.SZ_WHY_ENTITIES_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.Sz_whyEntities_V2_helper(
            entity_id_1,
            entity_id_2,
            flags,
        )
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    @catch_exceptions
    def why_records(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        flags: int = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.Sz_whyRecords_V2_helper(
            as_c_char_p(data_source_code_1),
            as_c_char_p(record_id_1),
            as_c_char_p(data_source_code_2),
            as_c_char_p(record_id_2),
            flags,
        )
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    @catch_exceptions
    def why_record_in_entity(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_WHY_RECORD_IN_ENTITY_DEFAULT_FLAGS,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.Sz_whyRecordInEntity_V2_helper(
            as_c_char_p(data_source_code),
            as_c_char_p(record_id),
            flags,
        )
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)
