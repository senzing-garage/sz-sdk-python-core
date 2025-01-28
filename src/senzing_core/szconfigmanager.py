"""
The `szconfigmanager` package is used to modify Senzing configurations in the Senzing database.
It is a wrapper over Senzing's SzConfigMgr C binding.
It conforms to the interface specified in
`szconfigmanager_abstract.py <https://github.com/senzing-garage/sz-sdk-python-core/blob/main/src/senzing_abstract/szconfigmanager_abstract.py>`_

To use szconfigmanager,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/er/lib
"""

# pylint: disable=R0903
from ctypes import POINTER, Structure, c_char, c_char_p, c_longlong, c_void_p
from functools import partial
from typing import Any, Dict, Union

from senzing import SzConfigManager

from ._helpers import (
    FreeCResources,
    as_c_char_p,
    as_python_str,
    as_str,
    catch_non_sz_exceptions,
    check_result_rc,
    load_sz_library,
)
from ._version import is_supported_senzingapi_version

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


class SzConfigMgrAddConfigResult(SzResponseLonglongReturnCodeResult):
    """In SzLang_helpers.h SzConfigMgr_addConfig_result"""


class SzConfigMgrGetConfigListResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h SzConfigMgr_getConfigList_result"""


class SzConfigMgrGetConfigResult(SzResponseReturnCodeResult):
    """In SzLang_helpers.h SzConfigMgr_getConfig_result"""


class SzConfigMgrGetDefaultConfigIDResult(SzResponseLonglongReturnCodeResult):
    """In SzLang_helpers.h SzConfigMgr_getDefaultConfigID_result"""


# -----------------------------------------------------------------------------
# SzConfigManagerCore class
# -----------------------------------------------------------------------------


class SzConfigManagerCore(SzConfigManager):
    """
    Use SzAbstractFactoryCore.create_configmanager() to create an SzConfigManager object.
    The SzConfigManager object uses the parameters provided to SzAbstractFactoryCore().

    Example:

    .. code-block:: python

        from senzing_core import SzAbstractFactoryCore

        sz_abstract_factory = SzAbstractFactoryCore(instance_name, settings)
        sz_config_manager = sz_abstract_factory.create_configmanager()

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
            self.library_handle.SzConfigMgr_getLastException,
            self.library_handle.SzConfigMgr_clearLastException,
            self.library_handle.SzConfigMgr_getLastExceptionCode,
        )

        # Initialize C function input parameters and results.
        # Synchronized with er/sdk/c/libSzConfigMgr.h

        self.library_handle.SzConfigMgr_addConfig_helper.argtypes = [c_char_p, c_char_p]
        self.library_handle.SzConfigMgr_addConfig_helper.restype = SzConfigMgrAddConfigResult
        self.library_handle.SzConfigMgr_destroy.argtypes = []
        self.library_handle.SzConfigMgr_destroy.restype = c_longlong
        self.library_handle.SzConfigMgr_getConfig_helper.argtypes = [c_longlong]
        self.library_handle.SzConfigMgr_getConfig_helper.restype = SzConfigMgrGetConfigResult
        self.library_handle.SzConfigMgr_getConfigList_helper.argtypes = []
        self.library_handle.SzConfigMgr_getConfigList_helper.restype = SzConfigMgrGetConfigListResult
        self.library_handle.SzConfigMgr_getDefaultConfigID_helper.restype = SzConfigMgrGetDefaultConfigIDResult
        self.library_handle.SzConfigMgr_init.argtypes = [c_char_p, c_char_p, c_longlong]
        self.library_handle.SzConfigMgr_init.restype = c_longlong
        self.library_handle.SzConfigMgr_replaceDefaultConfigID.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self.library_handle.SzConfigMgr_replaceDefaultConfigID.restype = c_longlong
        self.library_handle.SzConfigMgr_setDefaultConfigID.argtypes = [c_longlong]
        self.library_handle.SzConfigMgr_setDefaultConfigID.restype = c_longlong
        self.library_handle.SzHelper_free.argtypes = [c_void_p]

    def __del__(self) -> None:
        """Destructor"""

    # -------------------------------------------------------------------------
    # SzConfigManager methods
    # -------------------------------------------------------------------------

    @catch_non_sz_exceptions
    def add_config(
        self,
        config_definition: str,
        config_comment: str,
    ) -> int:
        result = self.library_handle.SzConfigMgr_addConfig_helper(
            as_c_char_p(config_definition),
            as_c_char_p(config_comment),
        )
        self.check_result(result.return_code)

        return result.response  # type: ignore[no-any-return]

    def _destroy(
        self,
    ) -> None:
        _ = self.library_handle.SzConfigMgr_destroy()

    @catch_non_sz_exceptions
    def get_config(self, config_id: int) -> str:
        result = self.library_handle.SzConfigMgr_getConfig_helper(config_id)
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    def get_configs(self) -> str:
        result = self.library_handle.SzConfigMgr_getConfigList_helper()
        with FreeCResources(self.library_handle, result.response):
            self.check_result(result.return_code)
            return as_python_str(result.response)

    def get_default_config_id(self) -> int:
        result = self.library_handle.SzConfigMgr_getDefaultConfigID_helper()
        self.check_result(result.return_code)
        return result.response  # type: ignore[no-any-return]

    @catch_non_sz_exceptions
    def _initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
    ) -> None:
        result = self.library_handle.SzConfigMgr_init(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            verbose_logging,
        )
        self.check_result(result)

    @catch_non_sz_exceptions
    def replace_default_config_id(
        self,
        current_default_config_id: int,
        new_default_config_id: int,
    ) -> None:
        result = self.library_handle.SzConfigMgr_replaceDefaultConfigID(
            current_default_config_id, new_default_config_id
        )
        self.check_result(result)

    @catch_non_sz_exceptions
    def set_default_config_id(self, config_id: int) -> None:
        result = self.library_handle.SzConfigMgr_setDefaultConfigID(config_id)
        self.check_result(result)
