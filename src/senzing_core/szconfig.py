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
    catch_sdk_exceptions,
    check_result_rc,
    load_sz_library,
)

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


class SzConfigCreateResult(SzResponseAsVoidPointerResult):
    """In SzLang_helpers.h SzConfig_create_result"""


class SzConfigExportResult(SzResponseAsCharPointerResult):
    """In SzLang_helpers.h SzConfig_export_result"""


class SzConfigGetDataSourceRegistryResult(SzResponseAsCharPointerResult):
    """In SzLang_helpers.h SzConfig_getDataSourceRegistry_result"""


class SzConfigLoadResult(SzResponseAsVoidPointerResult):
    """In SzLang_helpers.h SzConfig_load_result"""


class SzConfigRegisterDataSourceResult(SzResponseAsCharPointerResult):
    """In SzLang_helpers.h SzConfig_registerDataSource_result"""


# -----------------------------------------------------------------------------
# SzConfigCore class
# -----------------------------------------------------------------------------


class SzConfigCore(SzConfig):
    """
    Use SzAbstractFactoryCore.create_config() to create an SzConfig object.
    The SzConfig object uses the arguments provided to SzAbstractFactoryCore().

    Example:

    .. code-block:: python

        from senzing_core import SzAbstractFactoryCore

        sz_abstract_factory = SzAbstractFactoryCore(instance_name, settings)
        sz_config = sz_abstract_factory.create_config()

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

        # Partial function to use this modules self._library_handle for exception handling
        self._check_result = partial(
            check_result_rc,
            self._library_handle.SzConfig_getLastException,
            self._library_handle.SzConfig_clearLastException,
            self._library_handle.SzConfig_getLastExceptionCode,
        )

        # Initialize C function input parameters and results.
        # Synchronized with er/sdk/c/libSzConfig.h
        self._library_handle.SzConfig_close_helper.argtypes = [POINTER(c_uint)]
        self._library_handle.SzConfig_close_helper.restype = c_longlong
        self._library_handle.SzConfig_create_helper.argtypes = []
        self._library_handle.SzConfig_create_helper.restype = SzConfigCreateResult
        self._library_handle.SzConfig_destroy.argtypes = []
        self._library_handle.SzConfig_destroy.restype = c_longlong
        self._library_handle.SzConfig_export_helper.argtypes = [POINTER(c_uint)]
        self._library_handle.SzConfig_export_helper.restype = SzConfigExportResult
        self._library_handle.SzConfig_getDataSourceRegistry_helper.argtypes = [POINTER(c_uint)]
        self._library_handle.SzConfig_getDataSourceRegistry_helper.restype = SzConfigGetDataSourceRegistryResult
        self._library_handle.SzConfig_init.argtypes = [c_char_p, c_char_p, c_longlong]
        self._library_handle.SzConfig_init.restype = c_longlong
        self._library_handle.SzConfig_load_helper.argtypes = [c_char_p]
        self._library_handle.SzConfig_load_helper.restype = SzConfigLoadResult
        self._library_handle.SzConfig_registerDataSource_helper.argtypes = [
            POINTER(c_uint),
            c_char_p,
        ]
        self._library_handle.SzConfig_registerDataSource_helper.restype = SzConfigRegisterDataSourceResult
        self._library_handle.SzConfig_unregisterDataSource_helper.argtypes = [
            POINTER(c_uint),
            c_char_p,
        ]
        self._library_handle.SzConfig_unregisterDataSource_helper.restype = c_longlong
        self._library_handle.SzHelper_free.argtypes = [c_void_p]

        self.config_definition = ""

    # -------------------------------------------------------------------------
    # SzConfig interface methods
    # -------------------------------------------------------------------------

    @catch_sdk_exceptions
    def get_data_source_registry(self) -> str:
        # Create an in-memory representation of the Senzing configuration JSON.
        load_result = self._library_handle.SzConfig_load_helper(as_c_char_p(self.config_definition))
        self._check_result(load_result.return_code)
        config_handle = load_result.response

        # Get the list of datasources.
        get_data_source_registry_result = self._library_handle.SzConfig_getDataSourceRegistry_helper(
            as_c_uintptr_t(config_handle)
        )
        with FreeCResources(self._library_handle, get_data_source_registry_result.response):
            self._check_result(get_data_source_registry_result.return_code)
            result = as_python_str(get_data_source_registry_result.response)

        # Delete the in-memory representation of the Senzing configuration JSON.
        close_result = self._library_handle.SzConfig_close_helper(as_c_uintptr_t(config_handle))
        self._check_result(close_result)

        return result

    def export(self) -> str:
        return self.config_definition

    @catch_sdk_exceptions
    def register_data_source(
        self,
        data_source_code: str,
    ) -> str:
        # Create an in-memory representation of the Senzing configuration JSON.
        load_result = self._library_handle.SzConfig_load_helper(as_c_char_p(self.config_definition))
        self._check_result(load_result.return_code)
        config_handle = load_result.response

        # Register data source to in-memory representation of the Senzing configuration JSON.
        register_data_source_result = self._library_handle.SzConfig_registerDataSource_helper(
            as_c_uintptr_t(config_handle),
            as_c_char_p(build_dsrc_code_json(data_source_code)),
        )
        with FreeCResources(self._library_handle, register_data_source_result.response):
            self._check_result(register_data_source_result.return_code)
            result = as_python_str(register_data_source_result.response)

        # Export in-memory representation to a JSON document.
        save_result = self._library_handle.SzConfig_export_helper(as_c_uintptr_t(config_handle))
        with FreeCResources(self._library_handle, save_result.response):
            self._check_result(save_result.return_code)
            self.config_definition = as_python_str(save_result.response)

        # Delete the in-memory representation of the Senzing configuration JSON.
        close_result = self._library_handle.SzConfig_close_helper(as_c_uintptr_t(config_handle))
        self._check_result(close_result)

        return result

    @catch_sdk_exceptions
    def unregister_data_source(
        self,
        data_source_code: str,
    ) -> str:
        # Create an in-memory representation of the Senzing configuration JSON.
        load_result = self._library_handle.SzConfig_load_helper(as_c_char_p(self.config_definition))
        self._check_result(load_result.return_code)
        config_handle = load_result.response

        # Unregister data source from in-memory representation of the Senzing configuration JSON.
        unregister_data_source_result = self._library_handle.SzConfig_unregisterDataSource_helper(
            as_c_uintptr_t(config_handle),
            as_c_char_p(build_dsrc_code_json(data_source_code)),
        )
        self._check_result(unregister_data_source_result)

        # Export in-memory representation to a JSON document.
        save_result = self._library_handle.SzConfig_export_helper(as_c_uintptr_t(config_handle))
        with FreeCResources(self._library_handle, save_result.response):
            self._check_result(save_result.return_code)
            self.config_definition = as_python_str(save_result.response)

        # Delete the in-memory representation of the Senzing configuration JSON.
        close_result = self._library_handle.SzConfig_close_helper(as_c_uintptr_t(config_handle))
        self._check_result(close_result)

        return ""

    # -------------------------------------------------------------------------
    # Non-public SzConfigCore methods
    # -------------------------------------------------------------------------

    def _destroy(self) -> None:
        _ = self._library_handle.SzConfig_destroy()

    def import_config_definition(self, config_definition: str) -> None:
        """
        Set the internal JSON document.

        Args:
            config_definition (str): A Senzing configuration JSON document.
        """
        self.config_definition = config_definition

    @catch_sdk_exceptions
    def import_template(
        self,
    ) -> None:
        """
        Retrieves a Senzing configuration from the default template.
        The default template is the Senzing configuration JSON document file,
        g2config.json, located in the PIPELINE.RESOURCEPATH path.
        """
        create_result = self._library_handle.SzConfig_create_helper()
        self._check_result(create_result.return_code)
        config_handle = create_result.response

        # Export in-memory representation to a JSON document.
        save_result = self._library_handle.SzConfig_export_helper(as_c_uintptr_t(config_handle))
        with FreeCResources(self._library_handle, save_result.response):
            self._check_result(save_result.return_code)
            self.config_definition = as_python_str(save_result.response)

        # Delete the in-memory representation of the Senzing configuration JSON.
        close_result = self._library_handle.SzConfig_close_helper(as_c_uintptr_t(config_handle))
        self._check_result(close_result)

    @catch_sdk_exceptions
    def initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
    ) -> None:
        """
        Initialize the C-based Senzing SzConfig.

        Args:
            instance_name (str): A name to distinguish this instance of the SzConfig.
            settings (Union[str, Dict[Any, Any]]): A JSON document defining runtime configuration.
            verbose_logging (int, optional): Send debug statements to STDOUT. Defaults to 0.
        """
        result = self._library_handle.SzConfig_init(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            verbose_logging,
        )
        self._check_result(result)

    @catch_sdk_exceptions
    def verify_config_definition(self, config_definition: str) -> None:
        """
        Verify that a Senzing configuration JSON document is valid.
        This method does not update the internal Senzing configuration.
        If an error is not thrown, the Senzing configuration JSON is valid.
        """
        # Create an in-memory representation of the Senzing configuration JSON.
        load_result = self._library_handle.SzConfig_load_helper(as_c_char_p(config_definition))
        self._check_result(load_result.return_code)
        config_handle = load_result.response

        # Export in-memory representation to a JSON document.
        save_result = self._library_handle.SzConfig_export_helper(as_c_uintptr_t(config_handle))
        with FreeCResources(self._library_handle, save_result.response):
            self._check_result(save_result.return_code)
            _ = as_python_str(save_result.response)

        # Delete the in-memory representation of the Senzing configuration JSON.

        close_result = self._library_handle.SzConfig_close_helper(as_c_uintptr_t(config_handle))
        self._check_result(close_result)
