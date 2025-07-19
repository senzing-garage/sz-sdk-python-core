"""
``senzing_core.szconfigmanager.SzConfigManagerCore`` is an implementation
of the `senzing.szconfigmanager.SzConfigManager`_ interface that communicates with the Senzing binaries.

To use szconfigmanager,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/er/lib

.. _senzing.szconfigmanager.SzConfigManager: https://garage.senzing.com/sz-sdk-python/senzing.html#module-senzing.szconfigmanager
"""

# pylint: disable=R0903
from ctypes import POINTER, Structure, c_char, c_char_p, c_longlong, c_void_p
from functools import partial
from typing import Any, Dict, Union

from senzing import SzConfig, SzConfigManager

from ._helpers import (
    FreeCResources,
    as_c_char_p,
    as_python_str,
    as_str,
    catch_sdk_exceptions,
    check_is_destroyed,
    check_result_rc,
    load_sz_library,
)
from .szconfig import SzConfigCore

# Metadata

__all__ = ["SzConfigManagerCore"]
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


class SzConfigMgrGetConfigRegistryResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h SzConfigMgr_getConfigRegistry_result"""


class SzConfigMgrGetConfigResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h SzConfigMgr_getConfig_result"""


class SzConfigMgrGetDefaultConfigIDResult(SzResponseLonglongReturnCodeResult):
    """In SzLang_helpers.h SzConfigMgr_getDefaultConfigID_result"""


class SzConfigMgrRegisterConfigResult(SzResponseLonglongReturnCodeResult):
    """In SzLang_helpers.h SzConfigMgr_registerConfig_result"""


# -----------------------------------------------------------------------------
# SzConfigManagerCore class
# -----------------------------------------------------------------------------


class SzConfigManagerCore(SzConfigManager):
    """
    Use SzAbstractFactoryCore.create_configmanager() to create an SzConfigManager object.
    The SzConfigManager object uses the arguments provided to SzAbstractFactoryCore().

    Example:

    .. code-block:: python

        from senzing_core import SzAbstractFactoryCore

        sz_abstract_factory = SzAbstractFactoryCore(instance_name, settings)
        sz_config_manager = sz_abstract_factory.create_configmanager()

    Args:

    Raises:

    """

    # -------------------------------------------------------------------------
    # Dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(self, **kwargs: Any) -> None:
        _ = kwargs

        self._is_destroyed = False
        self._library_handle = load_sz_library()

        # Partial function to use this modules self._library_handle for exception handling
        self._check_result = partial(
            check_result_rc,
            self._library_handle.SzConfigMgr_getLastException,
            self._library_handle.SzConfigMgr_clearLastException,
            self._library_handle.SzConfigMgr_getLastExceptionCode,
        )

        # Initialize C function input parameters and results.
        # Synchronized with er/sdk/c/libSzConfigMgr.h
        self._library_handle.SzConfigMgr_destroy.argtypes = []
        self._library_handle.SzConfigMgr_destroy.restype = c_longlong
        self._library_handle.SzConfigMgr_getConfig_helper.argtypes = [c_longlong]
        self._library_handle.SzConfigMgr_getConfig_helper.restype = SzConfigMgrGetConfigResult
        self._library_handle.SzConfigMgr_getConfigRegistry_helper.argtypes = []
        self._library_handle.SzConfigMgr_getConfigRegistry_helper.restype = SzConfigMgrGetConfigRegistryResult
        self._library_handle.SzConfigMgr_getDefaultConfigID_helper.restype = SzConfigMgrGetDefaultConfigIDResult
        self._library_handle.SzConfigMgr_init.argtypes = [c_char_p, c_char_p, c_longlong]
        self._library_handle.SzConfigMgr_init.restype = c_longlong
        self._library_handle.SzConfigMgr_registerConfig_helper.argtypes = [c_char_p, c_char_p]
        self._library_handle.SzConfigMgr_registerConfig_helper.restype = SzConfigMgrRegisterConfigResult
        self._library_handle.SzConfigMgr_replaceDefaultConfigID.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self._library_handle.SzConfigMgr_replaceDefaultConfigID.restype = c_longlong
        self._library_handle.SzConfigMgr_setDefaultConfigID.argtypes = [c_longlong]
        self._library_handle.SzConfigMgr_setDefaultConfigID.restype = c_longlong
        self._library_handle.SzHelper_free.argtypes = [c_void_p]

        self.instance_name = ""
        self.settings = ""
        self.config_id = 0
        self.verbose_logging = 0

    @property
    def is_destroyed(self) -> bool:
        """Return if the instance has been destroyed."""
        return self._is_destroyed

    # -------------------------------------------------------------------------
    # SzConfigManager methods
    # -------------------------------------------------------------------------

    @check_is_destroyed
    @catch_sdk_exceptions
    def create_config_from_config_id(self, config_id: int) -> SzConfig:
        get_config_result = self._library_handle.SzConfigMgr_getConfig_helper(config_id)
        with FreeCResources(self._library_handle, get_config_result.response):
            self._check_result(get_config_result.return_code)
            config_definition = as_python_str(get_config_result.response)
        result = SzConfigCore()
        result.import_config_definition(config_definition)
        result._initialize(self.instance_name, self.settings, self.verbose_logging)  # pylint: disable=protected-access
        return result

    @check_is_destroyed
    @catch_sdk_exceptions
    def create_config_from_string(self, config_definition: str) -> SzConfig:
        result = SzConfigCore()
        result.verify_config_definition(config_definition)
        result.import_config_definition(config_definition)
        result._initialize(self.instance_name, self.settings, self.verbose_logging)  # pylint: disable=protected-access
        return result

    @check_is_destroyed
    @catch_sdk_exceptions
    def create_config_from_template(self) -> SzConfig:
        result = SzConfigCore()
        result._initialize(self.instance_name, self.settings, self.verbose_logging)  # pylint: disable=protected-access
        result.import_template()
        return result

    @check_is_destroyed
    def get_config_registry(self) -> str:
        result = self._library_handle.SzConfigMgr_getConfigRegistry_helper()
        with FreeCResources(self._library_handle, result.response):
            self._check_result(result.return_code)
            return as_python_str(result.response)

    @check_is_destroyed
    def get_default_config_id(self) -> int:
        result = self._library_handle.SzConfigMgr_getDefaultConfigID_helper()
        self._check_result(result.return_code)
        return result.response  # type: ignore[no-any-return]

    @check_is_destroyed
    @catch_sdk_exceptions
    def register_config(
        self,
        config_definition: str,
        config_comment: str,
    ) -> int:
        result = self._library_handle.SzConfigMgr_registerConfig_helper(
            as_c_char_p(config_definition),
            as_c_char_p(config_comment),
        )
        self._check_result(result.return_code)
        return result.response  # type: ignore[no-any-return]

    @check_is_destroyed
    @catch_sdk_exceptions
    def replace_default_config_id(
        self,
        current_default_config_id: int,
        new_default_config_id: int,
    ) -> None:
        result = self._library_handle.SzConfigMgr_replaceDefaultConfigID(
            current_default_config_id, new_default_config_id
        )
        self._check_result(result)

    @check_is_destroyed
    @catch_sdk_exceptions
    def set_default_config(self, config_definition: str, config_comment: str) -> int:
        config_id = self.register_config(config_definition, config_comment)
        self.set_default_config_id(config_id)
        return config_id

    @check_is_destroyed
    @catch_sdk_exceptions
    def set_default_config_id(self, config_id: int) -> None:
        result = self._library_handle.SzConfigMgr_setDefaultConfigID(config_id)
        self._check_result(result)

    # -------------------------------------------------------------------------
    # Public non-interface methods
    # -------------------------------------------------------------------------

    # NOTE - Not to use check_is_destroyed decorator
    def _destroy(self) -> None:
        if not self._is_destroyed:
            _ = self._library_handle.SzConfigMgr_destroy()
            self._is_destroyed = True

    # NOTE - Internal use only!
    def _internal_only_destroy(self) -> None:
        result = self._library_handle.SzConfigMgr_destroy()
        self._check_result(result)

    @check_is_destroyed
    @catch_sdk_exceptions
    def _initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
    ) -> None:
        self.instance_name = instance_name
        self.settings = as_str(settings)
        self.verbose_logging = verbose_logging
        result = self._library_handle.SzConfigMgr_init(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            verbose_logging,
        )
        self._check_result(result)
