"""
``senzing_core.szengine.SzEngineCore`` is an implementation
of the `senzing.szengine.SzEngine`_ interface that communicates with the Senzing binaries.

To use szengine,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/er/lib

.. _senzing.szengine.SzEngine: https://garage.senzing.com/sz-sdk-python/senzing.html#module-senzing.szengine
"""

# pylint: disable=R0903,C0302,R0915
# NOTE Used for ctypes type hinting - https://stackoverflow.com/questions/77619149/python-ctypes-pointer-type-hinting
from __future__ import annotations

from ctypes import (
    POINTER,
    Structure,
    c_char,
    c_char_p,
    c_longlong,
    c_uint,
    c_void_p,
    create_string_buffer,
)
from functools import partial
from typing import Any, Dict, List, Optional, Tuple, Union

from senzing import SZ_NO_INFO, SzEngine, SzEngineFlags

from ._helpers import (
    FreeCResources,
    as_c_char_p,
    as_c_uintptr_t,
    as_python_str,
    as_str,
    build_data_sources_json,
    build_entities_json,
    build_records_json,
    catch_sdk_exceptions,
    check_result_rc,
    load_sz_library,
)

# Metadata

__all__ = ["SzEngineCore"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2025-01-28"


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
    """In SzLang_helpers.h Sz_addRecordWithInfo_result"""


class SzDeleteRecordWithInfoResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_deleteRecordWithInfo_result"""


class SzExportCSVEntityReportResult(Structure):
    """In SzLang_helpers.h Sz_exportCSVEntityReport_result"""

    _fields_ = [
        ("export_handle", c_void_p),
        ("return_code", c_longlong),
    ]


class SzExportJSONEntityReportResult(Structure):
    """In SzLang_helpers.h Sz_exportJSONEntityReport_result"""

    _fields_ = [
        ("export_handle", c_void_p),
        ("return_code", c_longlong),
    ]


class SzFetchNextResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_fetchNext_result"""


class SzFindInterestingEntitiesByEntityIDResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_findInterestingEntitiesByEntityID_result"""


class SzFindInterestingEntitiesByRecordIDResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_findInterestingEntitiesByRecordID_result"""


class SzFindNetworkByEntityIDV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_findNetworkByEntityID_V2_result"""


class SzFindNetworkByRecordIDV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_findNetworkByRecordID_V2_result"""


class SzFindPathByEntityIDV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_findPathByEntityID_V2_result"""


class SzFindPathByRecordIDV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_findPathByRecordID_V2_result"""


class SzFindPathExcludingByEntityIDV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_findPathExcludingByEntityID_V2_result"""


class SzFindPathExcludingByRecordIDV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_findPathExcludingByRecordID_V2_result"""


class SzFindPathIncludingSourceByEntityIDV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_findPathIncludingSourceByEntityID_V2_result"""


class SzFindPathIncludingSourceByRecordIDV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_findPathIncludingSourceByRecordID_V2_result"""


class SzGetActiveConfigIDResult(SzResponseLonglongReturnCodeResult):
    """In SzLang_helpers.h Sz_getActiveConfigID_result"""


class SzGetEntityByEntityIDV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_getEntityByEntityID_V2_result"""


class SzGetEntityByRecordIDV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_getEntityByRecordID_V2_result"""


class SzGetRecordV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_getRecord_V2_result"""


class SzGetRecordPreviewResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_getRecordPreview_result"""


class SzGetRedoRecordResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_getRedoRecord_result"""


class SzGetVirtualEntityByRecordIDV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_getVirtualEntityByRecordID_V2_result"""


class SzHowEntityByEntityIDV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_howEntityByEntityID_V2_result"""


class SzProcessRedoRecordWithInfoResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_processRedoRecordWithInfo_result"""


class SzReevaluateEntityWithInfoResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_reevaluateEntityWithInfo_result"""


class SzReevaluateRecordWithInfoResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_reevaluateRecordWithInfo_result"""


class SzSearchByAttributesV3Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_searchByAttributes_V2_result"""


class SzStatsResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_stats_result"""


class SzWhyEntitiesV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_whyEntities_V2_result"""


class SzWhyRecordInEntityV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_whyRecordInEntity_V2_result"""


class SzWhyRecordsV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_whyRecords_V2_result"""


class SzWhySearchResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_whyEntities_result"""


class SzWhySearchV2Result(SzResponseReturnCodeResult):
    """In SzLang_helpers.h Sz_whyEntities_V2_result"""


# -----------------------------------------------------------------------------
# SzEngineCore class
# -----------------------------------------------------------------------------


class SzEngineCore(SzEngine):
    """
    Use SzAbstractFactoryCore.create_engine() to create an SzEngine object.
    The SzEngine object uses the arguments provided to SzAbstractFactoryCore().

    Example:

    .. code-block:: python

        from senzing_core import SzAbstractFactoryCore

        sz_abstract_factory = SzAbstractFactoryCore(instance_name, settings)
        sz_engine = sz_abstract_factory.create_engine()

    Args:

    Raises:

    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(self, **kwargs: Any) -> None:
        """Initializer"""

        _ = kwargs

        self._library_handle = load_sz_library()

        # Mask for removing SDK specific flags not supplied to method call
        self._sdk_flags_mask = ~(SzEngineFlags.SZ_WITH_INFO)

        # Partial function to use this modules self._library_handle for exception handling
        self._check_result = partial(
            check_result_rc,
            self._library_handle.Sz_getLastException,
            self._library_handle.Sz_clearLastException,
            self._library_handle.Sz_getLastExceptionCode,
        )

        # Initialize C function input parameters and results.
        # Must be synchronized with /opt/senzing/er/sdk/c/libSz.h
        self._library_handle.Szinternal_bulkLoad.argtypes = [POINTER(POINTER(c_char))]
        self._library_handle.Szinternal_bulkLoad.restype = c_longlong
        self._library_handle.Sz_addRecord.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
        ]
        self._library_handle.Sz_addRecord.restype = c_longlong
        self._library_handle.Sz_addRecordWithInfo_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_addRecordWithInfo_helper.restype = SzAddRecordWithInfoResult
        self._library_handle.Sz_closeExportReport_helper.argtypes = [
            POINTER(c_uint),
        ]
        self._library_handle.Sz_closeExportReport_helper.restype = c_longlong
        self._library_handle.Sz_countRedoRecords.argtypes = []
        self._library_handle.Sz_countRedoRecords.restype = c_longlong
        self._library_handle.Sz_deleteRecord.argtypes = [
            c_char_p,
            c_char_p,
        ]
        self._library_handle.Sz_deleteRecord.restype = c_longlong
        self._library_handle.Sz_deleteRecordWithInfo_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_deleteRecordWithInfo_helper.restype = SzDeleteRecordWithInfoResult
        self._library_handle.Sz_destroy.argtypes = []
        self._library_handle.Sz_destroy.restype = c_longlong
        self._library_handle.Sz_exportCSVEntityReport_helper.argtypes = [
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_exportCSVEntityReport_helper.restype = SzExportCSVEntityReportResult
        self._library_handle.Sz_exportJSONEntityReport_helper.argtypes = [c_longlong]
        self._library_handle.Sz_exportJSONEntityReport_helper.restype = SzExportJSONEntityReportResult
        self._library_handle.Sz_fetchNext_helper.argtypes = [
            POINTER(c_uint),
        ]
        self._library_handle.Sz_fetchNext_helper.restype = SzFetchNextResult
        self._library_handle.Sz_findInterestingEntitiesByEntityID_helper.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self._library_handle.Sz_findInterestingEntitiesByEntityID_helper.restype = (
            SzFindInterestingEntitiesByEntityIDResult
        )
        self._library_handle.Sz_findInterestingEntitiesByRecordID_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_findInterestingEntitiesByRecordID_helper.restype = (
            SzFindInterestingEntitiesByRecordIDResult
        )
        self._library_handle.Sz_findNetworkByEntityID_V2_helper.argtypes = [
            c_char_p,
            c_longlong,
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self._library_handle.Sz_findNetworkByEntityID_V2_helper.restype = SzFindNetworkByEntityIDV2Result
        self._library_handle.Sz_findNetworkByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_longlong,
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self._library_handle.Sz_findNetworkByRecordID_V2_helper.restype = SzFindNetworkByRecordIDV2Result
        self._library_handle.Sz_findPathByEntityID_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self._library_handle.Sz_findPathByEntityID_V2_helper.restype = SzFindPathByEntityIDV2Result
        self._library_handle.Sz_findPathByEntityIDIncludingSource_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_findPathByEntityIDIncludingSource_V2_helper.restype = (
            SzFindPathIncludingSourceByEntityIDV2Result
        )
        self._library_handle.Sz_findPathByEntityIDWithAvoids_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_findPathByEntityIDWithAvoids_V2_helper.restype = SzFindPathExcludingByEntityIDV2Result
        self._library_handle.Sz_findPathByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
            c_longlong,
        ]
        self._library_handle.Sz_findPathByRecordID_V2_helper.restype = SzFindPathByRecordIDV2Result
        self._library_handle.Sz_findPathByRecordIDIncludingSource_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_findPathByRecordIDIncludingSource_V2_helper.restype = (
            SzFindPathIncludingSourceByRecordIDV2Result
        )
        self._library_handle.Sz_findPathByRecordIDWithAvoids_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_findPathByRecordIDWithAvoids_V2_helper.restype = SzFindPathExcludingByRecordIDV2Result
        self._library_handle.Sz_getActiveConfigID_helper.argtypes = []
        self._library_handle.Sz_getActiveConfigID_helper.restype = SzGetActiveConfigIDResult
        self._library_handle.Sz_getEntityByEntityID_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self._library_handle.Sz_getEntityByEntityID_V2_helper.restype = SzGetEntityByEntityIDV2Result
        self._library_handle.Sz_getEntityByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_getEntityByRecordID_V2_helper.restype = SzGetEntityByRecordIDV2Result
        self._library_handle.Sz_getRecord_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_getRecord_V2_helper.restype = SzGetRecordV2Result
        self._library_handle.Sz_getRecordPreview_helper.argtypes = [
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_getRecordPreview_helper.restype = SzGetRecordPreviewResult
        self._library_handle.Sz_getRedoRecord_helper.argtypes = []
        self._library_handle.Sz_getRedoRecord_helper.restype = SzGetRedoRecordResult
        self._library_handle.Sz_getVirtualEntityByRecordID_V2_helper.argtypes = [
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_getVirtualEntityByRecordID_V2_helper.restype = SzGetVirtualEntityByRecordIDV2Result
        self._library_handle.Sz_howEntityByEntityID_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self._library_handle.Sz_howEntityByEntityID_V2_helper.restype = SzHowEntityByEntityIDV2Result
        self._library_handle.Sz_init.argtypes = [c_char_p, c_char_p, c_longlong]
        self._library_handle.Sz_init.restype = c_longlong
        self._library_handle.Sz_initWithConfigID.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
            c_longlong,
        ]
        self._library_handle.Sz_processRedoRecord.argtypes = [
            c_char_p,
        ]
        self._library_handle.Sz_processRedoRecord.restype = c_longlong
        self._library_handle.Sz_processRedoRecordWithInfo_helper.argtypes = [
            c_char_p,
        ]
        self._library_handle.Sz_processRedoRecordWithInfo_helper.restype = SzProcessRedoRecordWithInfoResult
        self._library_handle.Sz_reevaluateEntity.argtypes = [c_longlong, c_longlong]
        self._library_handle.Sz_reevaluateEntity.restype = c_longlong
        self._library_handle.Sz_reevaluateEntityWithInfo_helper.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self._library_handle.Sz_reevaluateEntityWithInfo_helper.restype = SzReevaluateEntityWithInfoResult
        self._library_handle.Sz_reevaluateRecord.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_reevaluateRecord.restype = c_longlong
        self._library_handle.Sz_reevaluateRecordWithInfo_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_reevaluateRecordWithInfo_helper.restype = SzReevaluateRecordWithInfoResult
        self._library_handle.Sz_reinit.argtypes = [c_longlong]
        self._library_handle.Sz_reinit.restype = c_longlong
        self._library_handle.Sz_searchByAttributes_V3_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_searchByAttributes_V3_helper.restype = SzSearchByAttributesV3Result
        self._library_handle.Sz_stats_helper.argtypes = []
        self._library_handle.Sz_stats_helper.restype = SzStatsResult
        self._library_handle.Sz_whyEntities_V2_helper.argtypes = [
            c_longlong,
            c_longlong,
            c_longlong,
        ]
        self._library_handle.Sz_whyEntities_V2_helper.restype = SzWhyEntitiesV2Result
        self._library_handle.Sz_whyRecordInEntity_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_whyRecords_V2_helper.restype = SzWhyRecordsV2Result
        self._library_handle.Sz_whyRecordInEntity_V2_helper.restype = SzWhyRecordInEntityV2Result
        self._library_handle.Sz_whyRecords_V2_helper.argtypes = [
            c_char_p,
            c_char_p,
            c_char_p,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.Sz_whySearch_helper.restype = SzWhySearchResult
        self._library_handle.Sz_whySearch_helper.argtypes = [
            c_char_p,
            c_longlong,
            c_char_p,
        ]
        self._library_handle.Sz_whySearch_V2_helper.restype = SzWhySearchV2Result
        self._library_handle.Sz_whySearch_V2_helper.argtypes = [
            c_char_p,
            c_longlong,
            c_char_p,
            c_longlong,
        ]
        self._library_handle.SzHelper_free.argtypes = [c_void_p]

    # -------------------------------------------------------------------------
    # SzEngine methods
    # -------------------------------------------------------------------------

    @catch_sdk_exceptions
    def _test_load(
        self,
        records: List[str],
    ) -> str:
        """Internal method for Senzing support"""
        try:
            c_records = (POINTER(c_char) * (len(records) + 1))()
            for idx, rec in enumerate(records):
                c_records[idx] = create_string_buffer(rec.encode())  # type: ignore[call-overload]
            c_records[len(records)] = None  # type: ignore[call-overload]

            result = self._library_handle.Szinternal_bulkLoad(c_records)
            self._check_result(result)
        except Exception as err:
            print(err)
            raise
        return SZ_NO_INFO

    @catch_sdk_exceptions
    def add_record(
        self,
        data_source_code: str,
        record_id: str,
        record_definition: str,
        flags: int = SzEngineFlags.SZ_ADD_RECORD_DEFAULT_FLAGS,
    ) -> str:
        if (flags & SzEngineFlags.SZ_WITH_INFO) != 0:
            result = self._library_handle.Sz_addRecordWithInfo_helper(
                as_c_char_p(data_source_code),
                as_c_char_p(record_id),
                as_c_char_p(record_definition),
                flags & self._sdk_flags_mask,
            )
            with FreeCResources(self._library_handle, result.response):
                self._check_result(result.return_code)
                return as_python_str(result.response)

        result = self._library_handle.Sz_addRecord(
            as_c_char_p(data_source_code),
            as_c_char_p(record_id),
            as_c_char_p(record_definition),
        )
        self._check_result(result)
        return SZ_NO_INFO

    @catch_sdk_exceptions
    def close_export_report(self, export_handle: int) -> None:
        result = self._library_handle.Sz_closeExportReport_helper(as_c_uintptr_t(export_handle))
        self._check_result(result)

    def count_redo_records(self) -> int:
        result: int = self._library_handle.Sz_countRedoRecords()
        if result < 0:
            self._check_result(result)
        return result

    @catch_sdk_exceptions
    def delete_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_DELETE_RECORD_DEFAULT_FLAGS,
    ) -> str:
        if (flags & SzEngineFlags.SZ_WITH_INFO) != 0:
            result = self._library_handle.Sz_deleteRecordWithInfo_helper(
                as_c_char_p(data_source_code),
                as_c_char_p(record_id),
                flags & self._sdk_flags_mask,
            )
            with FreeCResources(self._library_handle, result.response):
                self._check_result(result.return_code)
                return as_python_str(result.response)

        result = self._library_handle.Sz_deleteRecord(
            as_c_char_p(data_source_code),
            as_c_char_p(record_id),
        )
        self._check_result(result)
        return SZ_NO_INFO

    def _destroy(self) -> None:
        # TODO - Any other places in any engines we don't check_result?
        # _ = self._library_handle.Sz_destroy()
        print("HERE", flush=True)
        result = self._library_handle.Sz_destroy()
        self._check_result(result)

    @catch_sdk_exceptions
    def export_csv_entity_report(
        self,
        csv_column_list: str,
        flags: int = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS,
    ) -> int:
        result = self._library_handle.Sz_exportCSVEntityReport_helper(as_c_char_p(csv_column_list), flags)
        self._check_result(result.return_code)
        return result.export_handle  # type: ignore[no-any-return]

    def export_json_entity_report(
        self,
        flags: int = SzEngineFlags.SZ_EXPORT_DEFAULT_FLAGS,
    ) -> int:
        result = self._library_handle.Sz_exportJSONEntityReport_helper(flags)
        self._check_result(result.return_code)
        return result.export_handle  # type: ignore[no-any-return]

    @catch_sdk_exceptions
    def fetch_next(self, export_handle: int) -> str:
        result = self._library_handle.Sz_fetchNext_helper(as_c_uintptr_t(export_handle))
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    # NOTE Included but not documented or examples, early adaptor feature, needs manual additions to config
    @catch_sdk_exceptions
    def find_interesting_entities_by_entity_id(
        self, entity_id: int, flags: int = SzEngineFlags.SZ_FIND_INTERESTING_ENTITIES_DEFAULT_FLAGS
    ) -> str:
        result = self._library_handle.Sz_findInterestingEntitiesByEntityID_helper(entity_id, flags)
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    # NOTE Included but not documented or examples, early adaptor feature, needs manual additions to config
    @catch_sdk_exceptions
    def find_interesting_entities_by_record_id(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_FIND_INTERESTING_ENTITIES_DEFAULT_FLAGS,
    ) -> str:
        result = self._library_handle.Sz_findInterestingEntitiesByRecordID_helper(
            as_c_char_p(data_source_code), as_c_char_p(record_id), flags
        )
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @catch_sdk_exceptions
    def find_network_by_entity_id(
        self,
        entity_ids: List[int],
        max_degrees: int,
        build_out_degrees: int,
        build_out_max_entities: int,
        flags: int = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS,
    ) -> str:
        result = self._library_handle.Sz_findNetworkByEntityID_V2_helper(
            as_c_char_p(build_entities_json(entity_ids)),
            max_degrees,
            build_out_degrees,
            build_out_max_entities,
            flags,
        )

        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @catch_sdk_exceptions
    def find_network_by_record_id(
        self,
        record_keys: List[Tuple[str, str]],
        max_degrees: int,
        build_out_degrees: int,
        build_out_max_entities: int,
        flags: int = SzEngineFlags.SZ_FIND_NETWORK_DEFAULT_FLAGS,
    ) -> str:
        result = self._library_handle.Sz_findNetworkByRecordID_V2_helper(
            as_c_char_p(build_records_json(record_keys)),
            max_degrees,
            build_out_degrees,
            build_out_max_entities,
            flags,
        )
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @catch_sdk_exceptions
    def find_path_by_entity_id(
        self,
        start_entity_id: int,
        end_entity_id: int,
        max_degrees: int,
        avoid_entity_ids: Optional[List[int]] = None,
        required_data_sources: Optional[List[str]] = None,
        flags: int = SzEngineFlags.SZ_FIND_PATH_DEFAULT_FLAGS,
    ) -> str:
        if avoid_entity_ids and not required_data_sources:
            result = self._library_handle.Sz_findPathByEntityIDWithAvoids_V2_helper(
                start_entity_id,
                end_entity_id,
                max_degrees,
                as_c_char_p(build_entities_json(avoid_entity_ids)),
                flags,
            )
        elif required_data_sources:
            result = self._library_handle.Sz_findPathByEntityIDIncludingSource_V2_helper(
                start_entity_id,
                end_entity_id,
                max_degrees,
                as_c_char_p(build_entities_json(avoid_entity_ids)),
                as_c_char_p(build_data_sources_json(required_data_sources)),
                flags,
            )
        else:
            result = self._library_handle.Sz_findPathByEntityID_V2_helper(
                start_entity_id,
                end_entity_id,
                max_degrees,
                flags,
            )
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @catch_sdk_exceptions
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
    ) -> str:
        if avoid_record_keys and not required_data_sources:
            result = self._library_handle.Sz_findPathByRecordIDWithAvoids_V2_helper(
                as_c_char_p(start_data_source_code),
                as_c_char_p(start_record_id),
                as_c_char_p(end_data_source_code),
                as_c_char_p(end_record_id),
                max_degrees,
                as_c_char_p(build_records_json(avoid_record_keys)),
                flags,
            )
        elif required_data_sources:
            result = self._library_handle.Sz_findPathByRecordIDIncludingSource_V2_helper(
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
            result = self._library_handle.Sz_findPathByRecordID_V2_helper(
                as_c_char_p(start_data_source_code),
                as_c_char_p(start_record_id),
                as_c_char_p(end_data_source_code),
                as_c_char_p(end_record_id),
                max_degrees,
                flags,
            )
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    def get_active_config_id(self) -> int:
        result = self._library_handle.Sz_getActiveConfigID_helper()
        self._check_result(result.return_code)
        return result.response  # type: ignore[no-any-return]

    @catch_sdk_exceptions
    def get_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS,
    ) -> str:
        result = self._library_handle.Sz_getEntityByEntityID_V2_helper(entity_id, flags)
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @catch_sdk_exceptions
    def get_entity_by_record_id(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_ENTITY_DEFAULT_FLAGS,
    ) -> str:
        result = self._library_handle.Sz_getEntityByRecordID_V2_helper(
            as_c_char_p(data_source_code), as_c_char_p(record_id), flags
        )
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @catch_sdk_exceptions
    def get_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_RECORD_DEFAULT_FLAGS,
    ) -> str:
        result = self._library_handle.Sz_getRecord_V2_helper(
            as_c_char_p(data_source_code),
            as_c_char_p(record_id),
            flags,
        )
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @catch_sdk_exceptions
    def get_record_preview(
        self,
        record_definition: str,
        flags: int = SzEngineFlags.SZ_RECORD_PREVIEW_DEFAULT_FLAGS,
    ) -> str:
        result = self._library_handle.Sz_getRecordPreview_helper(
            as_c_char_p(record_definition),
            flags,
        )
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    def get_redo_record(self) -> str:
        result = self._library_handle.Sz_getRedoRecord_helper()
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    def get_stats(self) -> str:
        result = self._library_handle.Sz_stats_helper()
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @catch_sdk_exceptions
    def get_virtual_entity_by_record_id(
        self,
        record_keys: List[Tuple[str, str]],
        flags: int = SzEngineFlags.SZ_VIRTUAL_ENTITY_DEFAULT_FLAGS,
    ) -> str:
        result = self._library_handle.Sz_getVirtualEntityByRecordID_V2_helper(
            as_c_char_p(build_records_json(record_keys)),
            flags,
        )
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @catch_sdk_exceptions
    def how_entity_by_entity_id(
        self,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_HOW_ENTITY_DEFAULT_FLAGS,
    ) -> str:
        result = self._library_handle.Sz_howEntityByEntityID_V2_helper(entity_id, flags)
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @catch_sdk_exceptions
    def initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        config_id: int = 0,
        verbose_logging: int = 0,
    ) -> None:
        """
        Initialize the C-based Senzing SzEngine.

        Args:
            instance_name (str): A name to distinguish this instance of the SzEngine.
            settings (Union[str, Dict[Any, Any]]): A JSON document defining runtime configuration.
            config_id (int, optional): Initialize with a specific configuration ID. Defaults to current system DEFAULTCONFIGID.
            verbose_logging (int, optional): Send debug statements to STDOUT. Defaults to 0.
        """
        if config_id == 0:
            result = self._library_handle.Sz_init(
                as_c_char_p(instance_name),
                as_c_char_p(as_str(settings)),
                verbose_logging,
            )
            self._check_result(result)
            return

        result = self._library_handle.Sz_initWithConfigID(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            config_id,
            verbose_logging,
        )
        self._check_result(result)

    def prime_engine(self) -> None:
        result = self._library_handle.Sz_primeEngine()
        self._check_result(result)

    @catch_sdk_exceptions
    def process_redo_record(self, redo_record: str, flags: int = 0) -> str:
        if (flags & SzEngineFlags.SZ_WITH_INFO) != 0:
            result = self._library_handle.Sz_processRedoRecordWithInfo_helper(
                as_c_char_p(redo_record), flags & self._sdk_flags_mask
            )
            with FreeCResources(self._library_handle, result.response):
                self._check_result(result.return_code)
                return as_python_str(result.response)

        result = self._library_handle.Sz_processRedoRecord(
            as_c_char_p(redo_record),
        )
        self._check_result(result)
        return SZ_NO_INFO

    @catch_sdk_exceptions
    def reevaluate_entity(self, entity_id: int, flags: int = SzEngineFlags.SZ_REEVALUATE_RECORD_DEFAULT_FLAGS) -> str:
        if (flags & SzEngineFlags.SZ_WITH_INFO) != 0:
            result = self._library_handle.Sz_reevaluateEntityWithInfo_helper(
                entity_id,
                flags & self._sdk_flags_mask,
            )
            with FreeCResources(self._library_handle, result.response):
                self._check_result(result.return_code)
                response_str = as_python_str(result.response)
                return response_str if response_str else SZ_NO_INFO

        result = self._library_handle.Sz_reevaluateEntity(entity_id, flags)
        self._check_result(result)
        return SZ_NO_INFO

    @catch_sdk_exceptions
    def reevaluate_record(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_REEVALUATE_RECORD_DEFAULT_FLAGS,
    ) -> str:
        if (flags & SzEngineFlags.SZ_WITH_INFO) != 0:
            result = self._library_handle.Sz_reevaluateRecordWithInfo_helper(
                as_c_char_p(data_source_code),
                as_c_char_p(record_id),
                flags & self._sdk_flags_mask,
            )
            with FreeCResources(self._library_handle, result.response):
                self._check_result(result.return_code)
                response_str = as_python_str(result.response)
                return response_str if response_str else SZ_NO_INFO

        result = self._library_handle.Sz_reevaluateRecord(as_c_char_p(data_source_code), as_c_char_p(record_id), flags)
        self._check_result(result)
        return SZ_NO_INFO

    @catch_sdk_exceptions
    def reinitialize(self, config_id: int) -> None:
        """
        The `reinitialize` method reinitializes the Senzing object using a specific configuration
        identifier. A list of available configuration identifiers can be retrieved using
        `szconfigmanager.get_config_registry`.
        """
        result = self._library_handle.Sz_reinit(config_id)
        self._check_result(result)

    @catch_sdk_exceptions
    def search_by_attributes(
        self,
        attributes: str,
        flags: int = SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS,
        search_profile: str = "",
    ) -> str:
        result = self._library_handle.Sz_searchByAttributes_V3_helper(
            as_c_char_p(attributes),
            as_c_char_p(search_profile),
            flags,
        )
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @catch_sdk_exceptions
    def why_entities(
        self,
        entity_id_1: int,
        entity_id_2: int,
        flags: int = SzEngineFlags.SZ_WHY_ENTITIES_DEFAULT_FLAGS,
    ) -> str:
        result = self._library_handle.Sz_whyEntities_V2_helper(
            entity_id_1,
            entity_id_2,
            flags,
        )
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @catch_sdk_exceptions
    def why_records(
        self,
        data_source_code_1: str,
        record_id_1: str,
        data_source_code_2: str,
        record_id_2: str,
        flags: int = SzEngineFlags.SZ_WHY_RECORDS_DEFAULT_FLAGS,
    ) -> str:
        result = self._library_handle.Sz_whyRecords_V2_helper(
            as_c_char_p(data_source_code_1),
            as_c_char_p(record_id_1),
            as_c_char_p(data_source_code_2),
            as_c_char_p(record_id_2),
            flags,
        )
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @catch_sdk_exceptions
    def why_record_in_entity(
        self,
        data_source_code: str,
        record_id: str,
        flags: int = SzEngineFlags.SZ_WHY_RECORD_IN_ENTITY_DEFAULT_FLAGS,
    ) -> str:
        result = self._library_handle.Sz_whyRecordInEntity_V2_helper(
            as_c_char_p(data_source_code),
            as_c_char_p(record_id),
            flags,
        )
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @catch_sdk_exceptions
    def why_search(
        self,
        attributes: str,
        entity_id: int,
        flags: int = SzEngineFlags.SZ_WHY_SEARCH_DEFAULT_FLAGS,
        search_profile: str = "",
    ) -> str:
        result = self._library_handle.Sz_whySearch_V2_helper(
            as_c_char_p(attributes),
            entity_id,
            as_c_char_p(search_profile),
            flags,
        )
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)
