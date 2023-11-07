"""
The `g2config` package is used to modify the in-memory representation of a Senzing configuration.
It is a wrapper over Senzing's G2Config C binding.
It conforms to the interface specified in
`g2config_abstract.py <https://github.com/Senzing/g2-sdk-python-next/blob/main/src/senzing/g2config_abstract.py>`_

To use g2config,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/g2/lib
"""


import os
from ctypes import POINTER, c_char, c_char_p, c_longlong, c_size_t, cdll
from typing import Any

from .g2config_abstract import G2ConfigAbstract
from .g2exception import G2Exception, new_g2exception
from .g2helpers import find_file_in_path
from .g2version import is_supported_senzingapi_version

# Metadata

__all__ = ["G2Config"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

SENZING_PRODUCT_ID = "5040"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md
CALLER_SKIP = 6

# -----------------------------------------------------------------------------
# Classes that are result structures from calls to Senzing
# -----------------------------------------------------------------------------

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
        G2Exception: Raised when input parameters are incorrect.

    .. collapse:: Example:

        .. literalinclude:: ../../examples/g2config/g2config_constructor.py
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
        # Must be synchronized with g2/sdk/c/libg2config.h

        self.library_handle.G2Config_clearLastException.argtypes = []
        self.library_handle.G2Config_clearLastException.restype = None
        self.library_handle.G2Config_getLastException.argtypes = [
            POINTER(c_char),
            c_size_t,
        ]
        self.library_handle.G2Config_getLastException.restype = c_longlong
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

    def fake_g2config(self, *args: Any, **kwargs: Any) -> None:
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
        self, config_handle: int, input_json: str, *args: Any, **kwargs: Any
    ) -> str:
        self.fake_g2config(config_handle, input_json)
        return "string"

    def close(self, config_handle: int, *args: Any, **kwargs: Any) -> None:
        self.fake_g2config(config_handle)

    def create(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2config()
        return 0

    def delete_data_source(
        self, config_handle: int, input_json: str, *args: Any, **kwargs: Any
    ) -> None:
        self.fake_g2config(config_handle, input_json)

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        self.fake_g2config()

    def init(
        self,
        module_name: str,
        ini_params: str,
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        self.fake_g2config(module_name, ini_params, verbose_logging)

    def list_data_sources(self, config_handle: int, *args: Any, **kwargs: Any) -> str:
        self.fake_g2config(config_handle)
        return "string"

    def load(self, json_config: str, *args: Any, **kwargs: Any) -> int:
        self.fake_g2config(json_config)
        return 0

    def save(self, config_handle: int, *args: Any, **kwargs: Any) -> str:
        self.fake_g2config(config_handle)
        return "string"
