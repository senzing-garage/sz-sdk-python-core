"""
The `g2config` package is used to modify the in-memory representation of a Senzing configuration.
It is a wrapper over Senzing's G2Config C binding.
It conforms to the interface specified in
`g2config_abstract.py <https://github.com/senzing-garage/g2-sdk-python-next/blob/main/src/senzing/g2config_abstract.py>`_

To use g2config,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

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
    c_int,
    c_longlong,
    c_size_t,
    c_uint,
    c_void_p,
    cdll,
)
from typing import Any, Dict, Union

from .g2config_abstract import G2ConfigAbstract
from .g2exception import G2Exception, new_g2exception
from .g2helpers import (
    as_c_char_p,
    as_c_int,
    as_python_int,
    as_python_str,
    as_str,
    as_uintptr_t,
    find_file_in_path,
)
from .g2version import is_supported_senzingapi_version

# Metadata

__all__ = ["G2Config"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-07"

SENZING_PRODUCT_ID = "5040"  # See https://github.com/senzing-garage/knowledge-base/blob/main/lists/senzing-component-ids.md
CALLER_SKIP = 5

# -----------------------------------------------------------------------------
# Classes that are result structures from calls to Senzing
# -----------------------------------------------------------------------------


class G2ResponseAsCharPointerResult(Structure):
    """Simple response, return_code structure"""

    _fields_ = [
        ("response", POINTER(c_char)),
        ("return_code", c_longlong),
    ]


class G2ResponseAsVoidPointerResult(Structure):
    """Simple response, return_code structure"""

    _fields_ = [
        ("response", c_void_p),
        ("return_code", c_longlong),
    ]


class G2ConfigAddDataSourceResult(G2ResponseAsCharPointerResult):
    """In golang_helpers.h G2Config_addDataSource_result"""


class G2ConfigCreateResult(G2ResponseAsVoidPointerResult):
    """In golang_helpers.h G2Config_create_result"""


class G2ConfigListDataSourcesResult(G2ResponseAsCharPointerResult):
    """In golang_helpers.h G2Config_listDataSources_result"""


class G2ConfigLoadResult(G2ResponseAsVoidPointerResult):
    """In golang_helpers.h G2Config_load_result"""


class G2ConfigSaveResult(G2ResponseAsCharPointerResult):
    """In golang_helpers.h G2Config_save_result"""


# -----------------------------------------------------------------------------
# G2Config class
# -----------------------------------------------------------------------------


class G2Config(G2ConfigAbstract):
    """
    The `init` method initializes the Senzing G2Config object.
    It must be called prior to any other calls.

    **Note:** If the G2Config constructor is called with parameters,
    the constructor will automatically call the `init()` method.

    Example:

    .. code-block:: python

        g2_config = g2config.G2Config(module_name, ini_params)


    If the G2Config constructor is called without parameters,
    the `init()` method must be called to initialize the use of G2Product.

    Example:

    .. code-block:: python

        g2_config = g2config.G2Config()
        g2_config.init(module_name, ini_params)

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
        TypeError: Incorrect datatype detected on input parameter.
        g2exception.G2Exception: Failed to load the G2 library or incorrect `module_name`, `ini_params` combination.

    .. collapse:: Example:

        .. literalinclude:: ../../examples/g2config/g2config_constructor.py
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
        module_name: str = "",
        ini_params: Union[str, Dict[Any, Any]] = "",
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
        # TODO: Support init_config_id

        self.auto_init = False
        self.ini_params = as_str(ini_params)
        self.init_config_id = init_config_id
        self.module_name = module_name
        self.verbose_logging = verbose_logging

        # Determine if Senzing API version is acceptable.

        is_supported_senzingapi_version()

        # Load binary library.

        try:
            if os.name == "nt":
                # TODO: See if find_file_in_path can be factored out.
                self.library_handle = cdll.LoadLibrary(find_file_in_path("G2.dll"))
            else:
                self.library_handle = cdll.LoadLibrary("libG2.so")
        except OSError as err:
            raise G2Exception("Failed to load the G2 library") from err

        # Initialize C function input parameters and results.
        # Must be synchronized with g2/sdk/c/libg2config.h

        # self.library_handle.G2Config_addDataSource.argtypes = [c_void_p, c_char_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Config_addDataSource.restype = c_longlong
        self.library_handle.G2Config_addDataSource_helper.argtypes = [
            POINTER(c_uint),
            c_char_p,
        ]  # TODO: This may not be correct
        self.library_handle.G2Config_addDataSource_helper.restype = (
            G2ConfigAddDataSourceResult
        )
        self.library_handle.G2Config_clearLastException.argtypes = []
        self.library_handle.G2Config_clearLastException.restype = None
        # self.library_handle.G2Config_close.argtypes = [c_void_p]
        # self.library_handle.G2Config_close.restype = c_longlong
        self.library_handle.G2Config_close_helper.argtypes = [
            POINTER(c_uint)
        ]  # TODO: This may not be correct
        self.library_handle.G2Config_close_helper.restype = c_longlong
        # self.library_handle.G2Config_create.argtypes = [POINTER(c_void_p)]
        # self.library_handle.G2Config_create.restype = c_longlong
        self.library_handle.G2Config_create_helper.argtypes = []
        self.library_handle.G2Config_create_helper.restype = G2ConfigCreateResult
        # self.library_handle.G2Config_deleteDataSource.argtypes = [c_void_p, c_char_p]
        # self.library_handle.G2Config_deleteDataSource.restype = c_longlong
        self.library_handle.G2Config_deleteDataSource_helper.argtypes = [
            POINTER(c_uint),
            c_char_p,
        ]  # TODO: This may not be correct
        self.library_handle.G2Config_deleteDataSource_helper.restype = c_longlong
        self.library_handle.G2Config_destroy.argtypes = []
        self.library_handle.G2Config_destroy.restype = c_longlong
        self.library_handle.G2Config_getLastException.argtypes = [
            POINTER(c_char),
            c_size_t,
        ]
        self.library_handle.G2Config_getLastException.restype = c_longlong
        self.library_handle.G2Config_getLastExceptionCode.argtypes = []
        self.library_handle.G2Config_getLastExceptionCode.restype = c_longlong
        self.library_handle.G2Config_init.argtypes = [c_char_p, c_char_p, c_int]
        self.library_handle.G2Config_init.restype = c_longlong
        # self.library_handle.G2Config_listDataSources.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Config_listDataSources.restype = c_longlong
        self.library_handle.G2Config_listDataSources_helper.argtypes = [
            POINTER(c_uint)
        ]  # TODO: This may not be correct
        self.library_handle.G2Config_listDataSources_helper.restype = (
            G2ConfigListDataSourcesResult
        )
        # self.library_handle.G2Config_load.argtypes = [c_char_p, POINTER(c_void_p)]
        # self.library_handle.G2Config_load.restype = c_longlong
        self.library_handle.G2Config_load_helper.argtypes = [c_char_p]
        self.library_handle.G2Config_load_helper.restype = G2ConfigLoadResult
        # self.library_handle.G2Config_save.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t), self._resize_func_def]
        # self.library_handle.G2Config_save.restype = c_longlong
        self.library_handle.G2Config_save_helper.argtypes = [
            POINTER(c_uint)
        ]  # TODO: This may not be correct
        self.library_handle.G2Config_save_helper.restype = G2ConfigSaveResult
        self.library_handle.G2GoHelper_free.argtypes = [c_char_p]

        # Optionally, initialize Senzing engine.

        if (len(self.module_name) == 0) or (len(self.ini_params) == 0):
            if len(self.module_name) + len(self.ini_params) != 0:
                raise self.new_exception(4020, self.module_name, self.ini_params)
        if len(self.module_name) > 0:
            self.auto_init = True
            self.init(self.module_name, self.ini_params, self.verbose_logging)

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
        return new_g2exception(
            self.library_handle.G2Config_getLastException,
            self.library_handle.G2Config_clearLastException,
            SENZING_PRODUCT_ID,
            error_id,
            self.ID_MESSAGES,
            CALLER_SKIP,
            *args,
        )

    # -------------------------------------------------------------------------
    # G2Config methods
    # -------------------------------------------------------------------------

    def add_data_source(
        self,
        config_handle: int,
        input_json: Union[str, Dict[Any, Any]],
        *args: Any,
        **kwargs: Any,
    ) -> str:
        result = self.library_handle.G2Config_addDataSource_helper(
            as_uintptr_t(config_handle), as_c_char_p(as_str(input_json))
        )
        try:
            if result.return_code != 0:
                raise self.new_exception(
                    4001, config_handle, as_str(input_json), result.return_code
                )
            result_response = as_python_str(result.response)
        finally:
            self.library_handle.G2GoHelper_free(result.response)
        return result_response

    def close(self, config_handle: int, *args: Any, **kwargs: Any) -> None:
        result = self.library_handle.G2Config_close_helper(as_uintptr_t(config_handle))
        if result != 0:
            raise self.new_exception(4002, config_handle, result)

    def create(self, *args: Any, **kwargs: Any) -> int:
        result = self.library_handle.G2Config_create_helper()
        if result.return_code != 0:
            raise self.new_exception(4003, result.return_code)
        return as_python_int(result.response)

    def delete_data_source(
        self,
        config_handle: int,
        input_json: Union[str, Dict[Any, Any]],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        result = self.library_handle.G2Config_deleteDataSource_helper(
            as_uintptr_t(config_handle), as_c_char_p(as_str(input_json))
        )
        if result != 0:
            raise self.new_exception(
                4004, config_handle, as_str(input_json), result.return_code
            )

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        result = self.library_handle.G2Config_destroy()
        if result != 0:
            raise self.new_exception(4006, result)

    def init(
        self,
        module_name: str,
        ini_params: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        result = self.library_handle.G2Config_init(
            as_c_char_p(module_name),
            as_c_char_p(as_str(ini_params)),
            as_c_int(verbose_logging),
        )
        if result < 0:
            raise self.new_exception(
                4007, module_name, as_str(ini_params), verbose_logging, result
            )

    def list_data_sources(self, config_handle: int, *args: Any, **kwargs: Any) -> str:
        result = self.library_handle.G2Config_listDataSources_helper(
            as_uintptr_t(config_handle)
        )
        try:
            if result.return_code != 0:
                raise self.new_exception(4008, result.return_code)
            result_response = as_python_str(result.response)
        finally:
            self.library_handle.G2GoHelper_free(result.response)
        return result_response

    def load(
        self, json_config: Union[str, Dict[Any, Any]], *args: Any, **kwargs: Any
    ) -> int:
        result = self.library_handle.G2Config_load_helper(
            as_c_char_p(as_str(json_config))
        )
        if result.return_code != 0:
            raise self.new_exception(4009, as_str(json_config), result.return_code)
        return as_python_int(result.response)

    def save(self, config_handle: int, *args: Any, **kwargs: Any) -> str:
        result = self.library_handle.G2Config_save_helper(as_uintptr_t(config_handle))
        try:
            if result.return_code != 0:
                raise self.new_exception(4010, config_handle, result.return_code)
            result_response = as_python_str(result.response)
        finally:
            self.library_handle.G2GoHelper_free(result.response)
        return result_response
