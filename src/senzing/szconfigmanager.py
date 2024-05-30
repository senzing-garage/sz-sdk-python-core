"""
The `szconfigmanager` package is used to modify Senzing configurations in the Senzing database.
It is a wrapper over Senzing's G2Configmgr C binding.
It conforms to the interface specified in
`szconfigmanager_abstract.py <https://github.com/senzing-garage/sz-sdk-python/blob/main/src/senzing_abstract/szconfigmanager_abstract.py>`_

To use szconfigmanager,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/g2/lib
"""

# pylint: disable=R0903


import os
from contextlib import suppress
from ctypes import POINTER, Structure, c_char, c_char_p, c_longlong, cdll
from functools import partial
from types import TracebackType
from typing import Any, Dict, Type, Union

from senzing import SzConfigManagerAbstract, SzError, sdk_exception

from .szhelpers import (
    FreeCResources,
    as_c_char_p,
    as_python_str,
    as_str,
    catch_ctypes_exceptions,
    check_result_rc,
    find_file_in_path,
)
from .szversion import is_supported_senzingapi_version

# Metadata

__all__ = ["SzConfigManager"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-07"

SENZING_PRODUCT_ID = "5041"  # See https://github.com/senzing-garage/knowledge-base/blob/main/lists/senzing-component-ids.md

# -----------------------------------------------------------------------------
# Classes that are result structures from calls to Senzing
# -----------------------------------------------------------------------------


class G2ResponseReturnCodeResult(Structure):
    """Simple response, return_code structure"""

    _fields_ = [
        ("response", POINTER(c_char)),
        ("return_code", c_longlong),
    ]


class G2ResponseLonglongReturnCodeResult(Structure):
    """Simple response, return_code structure"""

    _fields_ = [
        ("response", c_longlong),
        ("return_code", c_longlong),
    ]


class G2ConfigMgrAddConfigResult(G2ResponseLonglongReturnCodeResult):
    """In golang_helpers.h G2ConfigMgr_addConfig_result"""


class G2ConfigMgrGetConfigListResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2ConfigMgr_getConfigList_result"""


class G2ConfigMgrGetConfigResult(G2ResponseReturnCodeResult):
    """In golang_helpers.h G2ConfigMgr_getConfig_result"""


class G2ConfigMgrGetDefaultConfigIDResult(G2ResponseLonglongReturnCodeResult):
    """In golang_helpers.h G2ConfigMgr_getDefaultConfigID_result"""


# -----------------------------------------------------------------------------
# SzConfigManager class
# -----------------------------------------------------------------------------


class SzConfigManager(SzConfigManagerAbstract):
    """
    The `initialize` method initializes the Senzing SzConfigManager object.
    It must be called prior to any other calls.

    **Note:** If the SzConfigManager constructor is called with parameters,
    the constructor will automatically call the `initialize()` method.

    Example:

    .. code-block:: python

        sz_configmanager = SzConfigManager(instance_name, settings)


    If the szconfigmanager constructor is called without parameters,
    the `initialize()` method must be called to initialize the use of SzConfigManager.

    Example:

    .. code-block:: python

        sz_configmanager = SzConfigManager()
        sz_configmanager.initialize(instance_name, settings)

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
            `Optional:` A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging. Default: 0

    Raises:
        TypeError: Incorrect datatype detected on input parameter.
        SzError: Failed to load the G2 library or incorrect `instance_name`, `settings` combination.

    .. collapse:: Example:

        .. literalinclude:: ../../examples/szconfigmanager/szconfigmanager_constructor.py
            :linenos:
            :language: python
    """

    # TODO: Consider making usual constructor private (`g2config.G2Config()`)
    # and replacing it with static constructor (i.e. `g2config.NewABC(str,str)`, `g2config.NewDEF(str,dict))

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        instance_name: str = "",
        settings: Union[str, Dict[Any, Any]] = "",
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """
        # pylint: disable=W0613

        self.auto_init = False
        self.settings = settings
        self.instance_name = instance_name
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
            # TODO: Change to Sz library when the libG2.so is changed in a build
            raise SzError("Failed to load the G2 library") from err

        # TODO Document what partial is...
        self.check_result = partial(
            check_result_rc,
            self.library_handle.G2ConfigMgr_getLastException,
            self.library_handle.G2ConfigMgr_clearLastException,
            self.library_handle.G2ConfigMgr_getLastExceptionCode,
            SENZING_PRODUCT_ID,
        )

        # Initialize C function input parameters and results.
        # Must be synchronized with g2/sdk/c/libg2configmgr.h

        self.library_handle.G2ConfigMgr_addConfig_helper.argtypes = [c_char_p, c_char_p]
        self.library_handle.G2ConfigMgr_addConfig_helper.restype = (
            G2ConfigMgrAddConfigResult
        )
        self.library_handle.G2ConfigMgr_destroy.argtypes = []
        self.library_handle.G2ConfigMgr_destroy.restype = c_longlong
        self.library_handle.G2ConfigMgr_getConfig_helper.argtypes = [c_longlong]
        self.library_handle.G2ConfigMgr_getConfig_helper.restype = (
            G2ConfigMgrGetConfigResult
        )
        self.library_handle.G2ConfigMgr_getConfigList_helper.argtypes = []
        self.library_handle.G2ConfigMgr_getConfigList_helper.restype = (
            G2ConfigMgrGetConfigListResult
        )
        self.library_handle.G2ConfigMgr_getDefaultConfigID_helper.restype = (
            G2ConfigMgrGetDefaultConfigIDResult
        )
        self.library_handle.G2ConfigMgr_init.argtypes = [c_char_p, c_char_p, c_longlong]
        self.library_handle.G2ConfigMgr_init.restype = c_longlong
        self.library_handle.G2ConfigMgr_replaceDefaultConfigID.argtypes = [
            c_longlong,
            c_longlong,
        ]
        self.library_handle.G2ConfigMgr_replaceDefaultConfigID.restype = c_longlong
        self.library_handle.G2ConfigMgr_setDefaultConfigID.argtypes = [c_longlong]
        self.library_handle.G2ConfigMgr_setDefaultConfigID.restype = c_longlong
        self.library_handle.G2GoHelper_free.argtypes = [c_char_p]

        # Optionally, initialize Senzing engine.

        if (len(self.instance_name) == 0) or (len(self.settings) == 0):
            if len(self.instance_name) + len(self.settings) != 0:
                raise sdk_exception(SENZING_PRODUCT_ID, 4001, 1)
        if len(self.instance_name) > 0:
            self.auto_init = True
            self.initialize(self.instance_name, self.settings, self.verbose_logging)

    def __del__(self) -> None:
        """Destructor"""
        if self.auto_init:
            with suppress(SzError):
                self.destroy()

    def __enter__(
        self,
    ) -> (
        Any
    ):  # TODO: Replace "Any" with "Self" once python 3.11 is lowest supported python version.
        """Context Manager method."""
        return self

    def __exit__(
        self,
        exc_type: Union[Type[BaseException], None],
        exc_val: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ) -> None:
        """Context Manager method."""

    # -------------------------------------------------------------------------
    # SzConfigManager methods
    # -------------------------------------------------------------------------

    @catch_ctypes_exceptions
    def add_config(
        self,
        config_definition: str,
        config_comment: str,
        **kwargs: Any,
    ) -> int:
        result = self.library_handle.G2ConfigMgr_addConfig_helper(
            as_c_char_p(config_definition),
            as_c_char_p(config_comment),
        )
        self.check_result(4002, result.return_code)

        return result.response  # type: ignore[no-any-return]

    def destroy(self, **kwargs: Any) -> None:
        result = self.library_handle.G2ConfigMgr_destroy()
        self.check_result(4003, result)

    def get_config(self, config_id: int, **kwargs: Any) -> str:
        result = self.library_handle.G2ConfigMgr_getConfig_helper(config_id)

        with FreeCResources(self.library_handle, result.response):
            self.check_result(4004, result.return_code)
            return as_python_str(result.response)

    def get_configs(self, **kwargs: Any) -> str:
        result = self.library_handle.G2ConfigMgr_getConfigList_helper()

        with FreeCResources(self.library_handle, result.response):
            self.check_result(4005, result.return_code)
            return as_python_str(result.response)

    def get_default_config_id(self, **kwargs: Any) -> int:
        result = self.library_handle.G2ConfigMgr_getDefaultConfigID_helper()
        self.check_result(4006, result.return_code)
        return result.response  # type: ignore[no-any-return]

    @catch_ctypes_exceptions
    def initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        result = self.library_handle.G2ConfigMgr_init(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            verbose_logging,
        )
        self.check_result(4007, result)

    def replace_default_config_id(
        self,
        current_default_config_id: int,
        new_default_config_id: int,
        **kwargs: Any,
    ) -> None:
        result = self.library_handle.G2ConfigMgr_replaceDefaultConfigID(
            current_default_config_id, new_default_config_id
        )
        self.check_result(4008, result)

    def set_default_config_id(self, config_id: int, **kwargs: Any) -> None:
        result = self.library_handle.G2ConfigMgr_setDefaultConfigID(config_id)
        self.check_result(4009, result)
