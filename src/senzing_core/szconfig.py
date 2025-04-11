#! /usr/bin/env python3

"""
``senzing_core.szconfig.SzConfigCore`` is an implementation
of the `senzing.szconfig.SzConfig`_ interface that communicates with the Senzing binaries.

To use szconfig,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/er/lib

.. _senzing.szconfig.SzConfig: https://garage.senzing.com/sz-sdk-python/senzing.html#module-senzing.szconfig
"""

# pylint: disable=R0903

from ctypes import POINTER, Structure, c_char, c_char_p, c_longlong, c_uint, c_void_p
from functools import partial
from typing import Any, Dict, Union

from senzing import SzConfig

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

__all__ = ["SzConfigCore"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2025-01-28"


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
# SzConfigCore class
# -----------------------------------------------------------------------------


class SzConfigCore(SzConfig):
    """
    Use SzAbstractFactoryCore.create_config() to create an SzConfig object.
    The SzConfig object uses the parameters provided to SzAbstractFactoryCore().

    Example:

    .. code-block:: python

        from senzing_core import SzAbstractFactoryCore

        sz_abstract_factory = SzAbstractFactoryCore(instance_name, settings)
        sz_config = sz_abstract_factory.create_config()

    Parameters:

    Raises:

    """

    # TODO: Consider making usual constructor private (`SzConfig.SzConfig()`)
    # and replacing it with static constructor (i.e. `SzConfig.NewABC(str,str)`, `SzConfig.NewDEF(str,dict))`

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

        self.config_definition = ""

        # if (not self.instance_name) or (len(self.settings) == 0):
        #     raise sdk_exception(2)

        # Initialize Senzing engine.
        # self._initialize(self.instance_name, self.settings, self.verbose_logging)
        # self.initialized = True

    def __del__(self) -> None:
        """Destructor"""

    # -------------------------------------------------------------------------
    # SzConfig interface methods
    # -------------------------------------------------------------------------

    @catch_non_sz_exceptions
    def add_data_source(
        self,
        data_source_code: str,
    ) -> str:
        # WORKING ON:

        # Create an in-memory representation of the Senzing configuration JSON.

        load_result = self.library_handle.SzConfig_load_helper(as_c_char_p(self.config_definition))
        with FreeCResources(self.library_handle, load_result.response):
            self.check_result(load_result.return_code)
            config_handle = load_result.response

        # Add DataSource to in-memory representation of the Senzing configuration JSON.

        add_data_source_result = self.library_handle.SzConfig_addDataSource_helper(
            as_c_uintptr_t(config_handle),
            as_c_char_p(build_dsrc_code_json(data_source_code)),
        )
        with FreeCResources(self.library_handle, add_data_source_result.response):
            self.check_result(add_data_source_result.return_code)
            result = add_data_source_result.response

        # Export in-memory representation to a JSON document.

        save_result = self.library_handle.SzConfig_save_helper(as_c_uintptr_t(config_handle))
        with FreeCResources(self.library_handle, save_result.response):
            self.check_result(save_result.return_code)
            self.config_definition = as_python_str(save_result.response)

        # Delete the in-memory representation of the Senzing configuration JSON.

        close_result = self.library_handle.SzConfig_close_helper(as_c_uintptr_t(config_handle))
        self.check_result(close_result)

        return result

    @catch_non_sz_exceptions
    def delete_data_source(
        self,
        data_source_code: str,
    ) -> None:

        # Create an in-memory representation of the Senzing configuration JSON.

        load_result = self.library_handle.SzConfig_load_helper(as_c_char_p(self.config_definition))
        with FreeCResources(self.library_handle, load_result.response):
            self.check_result(load_result.return_code)
            config_handle = load_result.response

        # Delete DataSource from in-memory representation of the Senzing configuration JSON.

        delete_data_source_result = self.library_handle.SzConfig_deleteDataSource_helper(
            as_c_uintptr_t(config_handle),
            as_c_char_p(build_dsrc_code_json(data_source_code)),
        )
        with FreeCResources(self.library_handle, delete_data_source_result.response):
            self.check_result(delete_data_source_result.return_code)
            result = delete_data_source_result.response

        # Export in-memory representation to a JSON document.

        save_result = self.library_handle.SzConfig_save_helper(as_c_uintptr_t(config_handle))
        with FreeCResources(self.library_handle, save_result.response):
            self.check_result(save_result.return_code)
            self.config_definition = as_python_str(save_result.response)

        # Delete the in-memory representation of the Senzing configuration JSON.

        close_result = self.library_handle.SzConfig_close_helper(as_c_uintptr_t(config_handle))
        self.check_result(close_result)

        return result

    def export(self) -> str:
        return self.config_definition

    @catch_non_sz_exceptions
    def get_data_sources(self) -> str:

        # Create an in-memory representation of the Senzing configuration JSON.

        load_result = self.library_handle.SzConfig_load_helper(as_c_char_p(self.config_definition))
        with FreeCResources(self.library_handle, load_result.response):
            self.check_result(load_result.return_code)
            config_handle = load_result.response

        # Get the list of datasources.

        list_data_sources_result = self.library_handle.SzConfig_listDataSources_helper(as_c_uintptr_t(config_handle))
        with FreeCResources(self.library_handle, list_data_sources_result.response):
            self.check_result(list_data_sources_result.return_code)
            result = as_python_str(list_data_sources_result.response)

        # Delete the in-memory representation of the Senzing configuration JSON.

        close_result = self.library_handle.SzConfig_close_helper(as_c_uintptr_t(config_handle))
        self.check_result(close_result)

        return result

    # -------------------------------------------------------------------------
    # Non-public SzConfigCore methods
    # -------------------------------------------------------------------------

    def _destroy(self) -> None:
        _ = self.library_handle.SzConfig_destroy()

    def import_config_definition(self, config_definition: str) -> None:
        self.config_definition = config_definition

    @catch_non_sz_exceptions
    def import_template(
        self,
    ) -> None:

        create_result = self.library_handle.SzConfig_create_helper()
        self.check_result(create_result.return_code)
        config_handle = create_result.response

        # Export in-memory representation to a JSON document.

        save_result = self.library_handle.SzConfig_save_helper(as_c_uintptr_t(config_handle))
        with FreeCResources(self.library_handle, save_result.response):
            self.check_result(save_result.return_code)
            self.config_definition = as_python_str(save_result.response)

        # Delete the in-memory representation of the Senzing configuration JSON.

        close_result = self.library_handle.SzConfig_close_helper(as_c_uintptr_t(config_handle))
        self.check_result(close_result)

    @catch_non_sz_exceptions
    def _initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
    ) -> None:
        result = self.library_handle.SzConfig_init(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            verbose_logging,
        )
        self.check_result(result)

    @catch_non_sz_exceptions
    def verify_config_definition(self, config_definition: str) -> None:
        """
        Verify that a Senzing configuration JSON document is valid.
        This method does not update the internal Senzing configuration.
        If an error is not thrown, the Senzing configuration JSON is valid.
        """

        # Create an in-memory representation of the Senzing configuration JSON.

        load_result = self.library_handle.SzConfig_load_helper(as_c_char_p(config_definition))
        with FreeCResources(self.library_handle, load_result.response):
            self.check_result(load_result.return_code)
            config_handle = load_result.response

        # Export in-memory representation to a JSON document.

        save_result = self.library_handle.SzConfig_save_helper(as_c_uintptr_t(config_handle))
        with FreeCResources(self.library_handle, save_result.response):
            self.check_result(save_result.return_code)
            _ = as_python_str(save_result.response)

        # Delete the in-memory representation of the Senzing configuration JSON.

        close_result = self.library_handle.SzConfig_close_helper(as_c_uintptr_t(config_handle))
        self.check_result(close_result)
