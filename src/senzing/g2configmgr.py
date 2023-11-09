"""
The `g2configmgr` package is used to modify Senzing configurations in the Senzing database.
It is a wrapper over Senzing's G2Configmgr C binding.
It conforms to the interface specified in
`g2configmgr_abstract.py <https://github.com/Senzing/g2-sdk-python-next/blob/main/src/senzing/g2configmgr_abstract.py>`_


To use g2configmgr,
the LD_LIBRARY_PATH environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/g2/lib
"""

# pylint: disable=R0903

import os
from ctypes import (
    POINTER,
    Structure,
    c_char,
    c_char_p,
    c_longlong,
    c_size_t,
    cast,
    cdll,
)
from typing import Any

from .g2configmgr_abstract import G2ConfigMgrAbstract
from .g2exception import G2Exception, new_g2exception
from .g2helpers import as_c_char_p, as_c_int, find_file_in_path
from .g2version import is_supported_senzingapi_version

# Metadata

__all__ = ["G2ConfigMgr"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-07"

SENZING_PRODUCT_ID = "5041"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md
CALLER_SKIP = 6

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
# G2ConfigMgr class
# -----------------------------------------------------------------------------


class G2ConfigMgr(G2ConfigMgrAbstract):
    """
    The `init` method initializes the Senzing G2ConfigMgr object.
    It must be called prior to any other calls.

    **Note:** If the G2ConfigMr constructor is called with parameters,
    the constructor will automatically call the `init()` method.

    Example:

    .. code-block:: python

        g2_configmgr = g2configmgr.G2ConfigMgr(module_name, ini_params)


    If the G2ConfigMgr constructor is called without parameters,
    the `init()` method must be called to initialize the use of G2Product.

    Example:

    .. code-block:: python

        g2_configmgr = g2configmgr.G2ConfigMgr()
        g2_configmgr.init(module_name, ini_params)

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

        .. literalinclude:: ../../examples/g2configmgr/g2configmgr_constructor.py
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
        # pylint: disable=W0613

        # Verify parameters.

        if (len(module_name) == 0) or (len(ini_params) == 0):
            if len(module_name) + len(ini_params) != 0:
                raise self.new_exception(9999, module_name, ini_params)

        self.ini_params = ini_params
        self.init_config_id = init_config_id
        self.module_name = module_name
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
            raise G2Exception("Failed to load the G2 library") from err

        # Initialize C function input parameters and results.
        # Must be synchronized with g2/sdk/c/libg2configmgr.h

        # self.library_handle.G2ConfigMgr_addConfig.argtypes = [c_char_p, c_char_p, POINTER(c_longlong)]
        # self.library_handle.G2ConfigMgr_addConfig.restype = c_longlong
        self.library_handle.G2ConfigMgr_addConfig_helper.argtypes = [c_char_p, c_char_p]
        self.library_handle.G2ConfigMgr_addConfig_helper.restype = (
            G2ConfigMgrAddConfigResult
        )
        self.library_handle.G2ConfigMgr_clearLastException.argtypes = []
        self.library_handle.G2ConfigMgr_clearLastException.restype = None
        self.library_handle.G2ConfigMgr_destroy.argtypes = []
        self.library_handle.G2ConfigMgr_destroy.restype = c_longlong
        # self.library_handle.G2ConfigMgr_getConfig.argtypes = [c_longlong, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2ConfigMgr_getConfig.restype = c_longlong
        self.library_handle.G2ConfigMgr_getConfig_helper.argtypes = [c_longlong]
        self.library_handle.G2ConfigMgr_getConfig_helper.restype = (
            G2ConfigMgrGetConfigResult
        )
        # self.library_handle.G2ConfigMgr_getConfigList.argtypes = [POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2ConfigMgr_getConfigList.restype = c_longlong
        self.library_handle.G2ConfigMgr_getConfigList_helper.argtypes = []
        self.library_handle.G2ConfigMgr_getConfigList_helper.restype = (
            G2ConfigMgrGetConfigListResult
        )
        # self.library_handle.G2ConfigMgr_getDefaultConfigID.argtypes = [POINTER(c_longlong)]
        # self.library_handle.G2ConfigMgr_getDefaultConfigID.restype = c_longlong
        self.library_handle.G2ConfigMgr_getDefaultConfigID_helper.argtypes = []
        self.library_handle.G2ConfigMgr_getDefaultConfigID_helper.restype = (
            G2ConfigMgrGetDefaultConfigIDResult
        )
        self.library_handle.G2ConfigMgr_getLastException.argtypes = [
            POINTER(c_char),
            c_size_t,
        ]
        self.library_handle.G2ConfigMgr_getLastException.restype = c_longlong
        self.library_handle.G2ConfigMgr_getLastExceptionCode.argtypes = []
        self.library_handle.G2ConfigMgr_getLastExceptionCode.restype = c_longlong
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

        # Initialize Senzing engine.

        if len(module_name) > 0:
            self.init(self.module_name, self.ini_params, self.verbose_logging)

    def __del__(self) -> None:
        """Destructor"""
        self.destroy()

    # -------------------------------------------------------------------------
    # Development methods - to be removed after initial development
    # -------------------------------------------------------------------------

    def fake_g2configmgr(self, *args: Any, **kwargs: Any) -> None:
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
            self.library_handle.G2ConfigMgr_getLastException,
            self.library_handle.G2ConfigMgr_clearLastException,
            SENZING_PRODUCT_ID,
            error_id,
            self.ID_MESSAGES,
            CALLER_SKIP,
            *args,
        )

    # -------------------------------------------------------------------------
    # G2ConfigMgr methods
    # -------------------------------------------------------------------------

    def add_config(
        self, config_str: str, config_comments: str, *args: Any, **kwargs: Any
    ) -> int:
        self.fake_g2configmgr(config_str, config_comments)
        return 0

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        self.fake_g2configmgr()

    def get_config(self, config_id: int, *args: Any, **kwargs: Any) -> str:
        self.fake_g2configmgr(config_id)
        return "string"

    def get_config_list(self, *args: Any, **kwargs: Any) -> str:
        result = self.library_handle.G2ConfigMgr_getConfigList_helper()
        try:
            if result.return_code != 0:
                raise self.new_exception(4004, result.return_code)
            result_response = cast(result.response, c_char_p).value
            result_response_str = result_response.decode() if result_response else ""
        finally:
            self.library_handle.G2GoHelper_free(result.response)
        return result_response_str

    def get_default_config_id(self, *args: Any, **kwargs: Any) -> int:
        result = self.library_handle.G2ConfigMgr_getDefaultConfigID_helper()
        if result.return_code != 0:
            # TODO: 4007?
            raise self.new_exception(4005, result.return_code)
        return int(result.response)

    def init(
        self,
        module_name: str,
        ini_params: str,
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        # self.fake_g2configmgr(module_name, ini_params, verbose_logging)
        result = self.library_handle.G2ConfigMgr_init(
            as_c_char_p(module_name),
            as_c_char_p(ini_params),
            as_c_int(verbose_logging),
        )
        if result < 0:
            raise self.new_exception(
                4007, module_name, ini_params, verbose_logging, result
            )

    def replace_default_config_id(
        self, old_config_id: int, new_config_id: int, *args: Any, **kwargs: Any
    ) -> None:
        self.fake_g2configmgr(old_config_id, new_config_id)

    def set_default_config_id(self, config_id: int, *args: Any, **kwargs: Any) -> None:
        self.fake_g2configmgr(config_id)
