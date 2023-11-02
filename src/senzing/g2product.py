"""
The g2product package is used to inspect the Senzing product.
It is a wrapper over Senzing's G2Product C binding.
It conforms to the interface specified in
`g2product_abstract.py <https://github.com/Senzing/g2-sdk-python-next/blob/main/src/senzing/g2product_abstract.py>`_

To use g2product,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/g2/lib
"""

import os
from ctypes import POINTER, c_char, c_char_p, c_int, c_longlong, c_size_t, cdll
from typing import Any

from .g2exception import G2Exception, new_g2exception
from .g2helpers import as_normalized_int, as_normalized_string, find_file_in_path
from .g2product_abstract import G2ProductAbstract

# Metadata

__all__ = ["G2Product"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

SENZING_PRODUCT_ID = "5046"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md
CALLER_SKIP = 6  # Number of stack frames to skip when reporting location in Exception.

# -----------------------------------------------------------------------------
# G2Product class
# -----------------------------------------------------------------------------


class G2Product(G2ProductAbstract):
    """
    The `init` method initializes the Senzing G2Product object.
    It must be called prior to any other calls.

    **Note:** If the G2Product constructor is called with parameters,
    the constructor will automatically call the `init()` method.

    Example:

    .. code-block:: python

        g2_product = g2product.G2Product(ENGINE_MODULE_NAME, ENGINE_CONFIGURATION_JSON)


    If the G2Product constructor is called without parameters,
    the `init()` method must be called to initialize the use of G2Product.

    Example:

    .. code-block:: python

        g2_product = g2product.G2Product()
        g2_product.init(ENGINE_MODULE_NAME, ENGINE_CONFIGURATION_JSON, ENGINE_VERBOSE_LOGGING)

    Either `module_name` and `ini_params` must both be specified or neither must be specified.
    Just specifying one or the other results in a **G2Exception**.

    Parameters:
        module_name:
            `Optional:` A name for the auditing node, to help identify it within system logs. Default: ""
        ini_params:
            `Optional:` A JSON string containing configuration parameters. Default: ""
        init_config_id:
            `Optional:` Specify the ID of a specific Senzing configuration. Default: 0 - Use current Senzing configuration
        verbose_logging:
            `Optional:` A flag to enable deeper logging of the G2 processing. 0 for no Senzing logging; 1 for logging. Default: 0

    Raises:
        G2Exception: Raised when input parameters are incorrect.

    .. collapse:: Example:

        .. literalinclude:: ../../examples/g2product_constructor.py
            :linenos:
            :language: python
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        *args: Any,
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

        # Verify parameters.

        if (len(module_name) == 0) or (len(ini_params) == 0):
            if len(module_name) + len(ini_params) != 0:
                raise self.new_exception(4004, module_name, ini_params)

        self.ini_params = ini_params
        self.module_name = module_name
        self.init_config_id = init_config_id
        self.verbose_logging = verbose_logging

        # Load binary library.

        try:
            if os.name == "nt":
                self.library_handle = cdll.LoadLibrary(find_file_in_path("G2.dll"))
            else:
                self.library_handle = cdll.LoadLibrary("libG2.so")
        except OSError as err:
            raise G2Exception("Failed to load the G2 library") from err

        # Initialize C function input parameters and results
        # Must be synchronized with g2/sdk/c/libg2product.h

        self.library_handle.G2GoHelper_free.argtypes = [c_char_p]
        self.library_handle.G2Product_clearLastException.argtypes = []
        self.library_handle.G2Product_clearLastException.restype = None
        self.library_handle.G2Product_destroy.argtypes = []
        self.library_handle.G2Product_destroy.restype = c_longlong
        self.library_handle.G2Product_getLastException.argtypes = [
            POINTER(c_char),
            c_size_t,
        ]
        self.library_handle.G2Product_getLastException.restype = c_longlong
        self.library_handle.G2Product_init.argtypes = [
            c_char_p,
            c_char_p,
            c_int,
        ]
        self.library_handle.G2Product_init.restype = c_longlong
        self.library_handle.G2Product_license.argtypes = []
        self.library_handle.G2Product_license.restype = c_char_p
        self.library_handle.G2Product_version.argtypes = []
        self.library_handle.G2Product_version.restype = c_char_p

        # Optionally, initialize Senzing engine.

        if len(module_name) > 0:
            self.init(self.module_name, self.ini_params, self.verbose_logging)

    def __del__(self) -> None:
        """Destructor"""
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
            self.library_handle.G2Product_getLastException,
            self.library_handle.G2Product_clearLastException,
            SENZING_PRODUCT_ID,
            error_id,
            self.ID_MESSAGES,
            CALLER_SKIP,
            *args,
        )

    # -------------------------------------------------------------------------
    # G2Product methods
    # -------------------------------------------------------------------------

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        result = self.library_handle.G2Product_destroy()
        if result != 0:
            raise self.new_exception(4001, result)

    def init(
        self,
        module_name: str,
        ini_params: str,
        *args: Any,
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        result = self.library_handle.G2Product_init(
            as_normalized_string(module_name),
            as_normalized_string(ini_params),
            as_normalized_int(verbose_logging),
        )
        if result < 0:
            raise self.new_exception(
                4003, module_name, ini_params, verbose_logging, result
            )

    def license(self, *args: Any, **kwargs: Any) -> str:
        return str(self.library_handle.G2Product_license().decode())

    def version(self, *args: Any, **kwargs: Any) -> str:
        return str(self.library_handle.G2Product_version().decode())
