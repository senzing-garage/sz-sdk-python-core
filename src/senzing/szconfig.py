"""
The `szconfig` package is used to modify the in-memory representation of a Senzing configuration.
It is a wrapper over Senzing's SzConfig C binding.
It conforms to the interface specified in
`szconfig_abstract.py <https://github.com/senzing-garage/sz-sdk-python/blob/main/src/senzing_abstract/szconfig_abstract.py>`_

To use szconfig,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/er/lib
"""

# pylint: disable=R0903

from ctypes import POINTER, Structure, c_char, c_char_p, c_longlong, c_uint, c_void_p
from functools import partial
from typing import Any, Dict, Union

from senzing_abstract import SzConfigAbstract

from ._helpers import (
    FreeCResources,
    as_c_char_p,
    as_c_uintptr_t,
    as_python_str,
    as_str,
    build_dsrc_code_json,
    catch_non_sz_exceptions,
    check_result_rc,
    load_sz_library,
)
from ._version import is_supported_senzingapi_version

# Metadata

__all__ = ["SzConfig"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-07"


# -----------------------------------------------------------------------------
# Classes that are result structures from calls to Senzing
# -----------------------------------------------------------------------------


class SzResponseAsCharPointerResult(Structure):
    """Simple response, return_code structure"""

    _fields_ = [
        ("response", POINTER(c_char)),
        ("return_code", c_longlong),
    ]


class SzResponseAsVoidPointerResult(Structure):
    """Simple response, return_code structure"""

    _fields_ = [
        ("response", c_void_p),
        ("return_code", c_longlong),
    ]


class SzConfigAddDataSourceResult(SzResponseAsCharPointerResult):
    """In SzLang_helpers.h SzConfig_addDataSource_result"""


class SzConfigCreateResult(SzResponseAsVoidPointerResult):
    """In SzLang_helpers.h SzConfig_create_result"""


class SzConfigListDataSourcesResult(SzResponseAsCharPointerResult):
    """In SzLang_helpers.h SzConfig_listDataSources_result"""


class SzConfigLoadResult(SzResponseAsVoidPointerResult):
    """In SzLang_helpers.h SzConfig_load_result"""


class SzConfigSaveResult(SzResponseAsCharPointerResult):
    """In SzLang_helpers.h SzConfig_save_result"""


# -----------------------------------------------------------------------------
# SzConfig class
# -----------------------------------------------------------------------------


class SzConfig(SzConfigAbstract):
    """
    Use SzAbstractFactory.create_sz_config() to create an SzConfig object.
    The SzConfig object uses the parameters provided to the SzAbstractFactory()
    function.

    Example:

    .. code-block:: python

        sz_abstract_factory = SzAbstractFactory(instance_name, settings)
        sz_config = sz_abstract_factory.create_sz_config()

    Parameters:

    Raises:

    """

    # TODO: Consider making usual constructor private (`SzConfig.SzConfig()`)
    # and replacing it with static constructor (i.e. `SzConfig.NewABC(str,str)`, `SzConfig.NewDEF(str,dict))

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """

        # Determine if Senzing API version is acceptable.
        is_supported_senzingapi_version()

        # Load binary library.
        self.library_handle = load_sz_library()

        # Partial function to use this modules self.library_handle for exception handling
        self.check_result = partial(
            check_result_rc,
            self.library_handle.SzConfig_getLastException,
            self.library_handle.SzConfig_clearLastException,
            self.library_handle.SzConfig_getLastExceptionCode,
        )

        # Initialize C function input parameters and results.
        # Synchronized with er/sdk/c/libSzConfig.h

        self.library_handle.SzConfig_addDataSource_helper.argtypes = [
            POINTER(c_uint),
            c_char_p,
        ]
        self.library_handle.SzConfig_addDataSource_helper.restype = SzConfigAddDataSourceResult
        self.library_handle.SzConfig_close_helper.argtypes = [POINTER(c_uint)]
        self.library_handle.SzConfig_close_helper.restype = c_longlong
        self.library_handle.SzConfig_create_helper.argtypes = []
        self.library_handle.SzConfig_create_helper.restype = SzConfigCreateResult
        self.library_handle.SzConfig_deleteDataSource_helper.argtypes = [
            POINTER(c_uint),
            c_char_p,
        ]
        self.library_handle.SzConfig_deleteDataSource_helper.restype = c_longlong
        self.library_handle.SzConfig_destroy.argtypes = []
        self.library_handle.SzConfig_destroy.restype = c_longlong
        self.library_handle.SzConfig_init.argtypes = [c_char_p, c_char_p, c_longlong]
        self.library_handle.SzConfig_init.restype = c_longlong
        self.library_handle.SzConfig_listDataSources_helper.argtypes = [POINTER(c_uint)]
        self.library_handle.SzConfig_listDataSources_helper.restype = SzConfigListDataSourcesResult
        self.library_handle.SzConfig_load_helper.argtypes = [c_char_p]
        self.library_handle.SzConfig_load_helper.restype = SzConfigLoadResult
        self.library_handle.SzConfig_save_helper.argtypes = [POINTER(c_uint)]
        self.library_handle.SzConfig_save_helper.restype = SzConfigSaveResult
        self.library_handle.SzHelper_free.argtypes = [c_void_p]

        # if (not self.instance_name) or (len(self.settings) == 0):
        #     raise sdk_exception(2)

        # Initialize Senzing engine.
        # self._initialize(self.instance_name, self.settings, self.verbose_logging)
        # self.initialized = True

    def __del__(self) -> None:
        """Destructor"""

    # -------------------------------------------------------------------------
    # SzConfig methods
    # -------------------------------------------------------------------------

    @catch_non_sz_exceptions
    def add_data_source(
        self,
        config_handle: int,
        data_source_code: str,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.SzConfig_addDataSource_helper(
            as_c_uintptr_t(config_handle),
            as_c_char_p(build_dsrc_code_json(data_source_code)),
        )

        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    @catch_non_sz_exceptions
    def close_config(self, config_handle: int, **kwargs: Any) -> None:
        result = self.library_handle.SzConfig_close_helper(as_c_uintptr_t(config_handle))
        self.check_result(result)

    def create_config(self, **kwargs: Any) -> int:
        result = self.library_handle.SzConfig_create_helper()
        self.check_result(result.return_code)
        return result.response  # type: ignore[no-any-return]

    @catch_non_sz_exceptions
    def delete_data_source(
        self,
        config_handle: int,
        data_source_code: str,
        **kwargs: Any,
    ) -> None:
        result = self.library_handle.SzConfig_deleteDataSource_helper(
            as_c_uintptr_t(config_handle),
            as_c_char_p(build_dsrc_code_json(data_source_code)),
        )
        self.check_result(result)

    def _destroy(self, **kwargs: Any) -> None:
        _ = self.library_handle.SzConfig_destroy()

    @catch_non_sz_exceptions
    def export_config(self, config_handle: int, **kwargs: Any) -> str:
        result = self.library_handle.SzConfig_save_helper(as_c_uintptr_t(config_handle))
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    @catch_non_sz_exceptions
    def get_data_sources(self, config_handle: int, **kwargs: Any) -> str:
        result = self.library_handle.SzConfig_listDataSources_helper(as_c_uintptr_t(config_handle))
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    @catch_non_sz_exceptions
    def _initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        result = self.library_handle.SzConfig_init(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            verbose_logging,
        )
        self.check_result(result)

    @catch_non_sz_exceptions
    def import_config(self, config_definition: str, **kwargs: Any) -> int:
        result = self.library_handle.SzConfig_load_helper(as_c_char_p(config_definition))
        self.check_result(result.return_code)
        return result.response  # type: ignore[no-any-return]
