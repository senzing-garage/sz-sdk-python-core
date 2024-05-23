"""
The `szproduct` package is used to inspect the Senzing product.
It is a wrapper over Senzing's G2Product C binding.
It conforms to the interface specified in
`szproduct_abstract.py <https://github.com/senzing-garage/sz-sdk-python/blob/main/src/senzing_abstract/szproduct_abstract.py>`_

To use szproduct,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/g2/lib
"""

# pylint: disable=R0903


import os
from ctypes import c_char_p, c_int, c_longlong, cdll
from types import TracebackType
from typing import Any, Dict, Type, Union

from senzing import (
    SzError,
    SzProductAbstract,
    as_c_char_p,
    as_python_str,
    as_str,
    catch_ctypes_exceptions,
    find_file_in_path,
    new_szexception,
)

# Metadata

__all__ = ["SzProduct"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-07"

SENZING_PRODUCT_ID = "5046"  # See https://github.com/senzing-garage/knowledge-base/blob/main/lists/senzing-component-ids.md

# -----------------------------------------------------------------------------
# SzProduct class
# -----------------------------------------------------------------------------


class SzProduct(SzProductAbstract):
    """
    The `init` method initializes the Senzing SzProduct object.
    It must be called prior to any other calls.

    **Note:** If the SzProduct constructor is called with parameters,
    the constructor will automatically call the `initialize()` method.

    Example:

    .. code-block:: python

        sz_product = SzProduct(instance_name, settings)


    If the SzProduct constructor is called without parameters,
    the `initialize()` method must be called to initialize the use of SzProduct.

    Example:

    .. code-block:: python

        sz_product = SzProduct()
        sz_product.initialize(instance_name, settings)

    Either `instance_name` and `settings` must both be specified or neither must be specified.
    Just specifying one or the other results in a **SzError**.

    Parameters:
        instance_name:
            `Optional:` A name for the auditing node, to help identify it within system logs. Default: ""
        settings:
            `Optional:` A JSON string containing configuration parameters. Default: ""
        verbose_logging:
            `Optional:` A flag to enable deeper logging of the Senzing processing. 0 for no Senzing logging; 1 for logging. Default: 0

    Raises:
        TypeError: Incorrect datatype detected on input parameter.
        SzError: Failed to load the Senzing library or incorrect `instance_name`, `settings` combination.

    .. collapse:: Example:

        .. literalinclude:: ../../examples/szproduct/szproduct_constructor.py
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

        # Verify parameters.

        self.auto_init = False
        # self.settings = as_str(settings)
        self.settings = settings
        self.instance_name = instance_name
        self.verbose_logging = verbose_logging

        # Load binary library.

        try:
            if os.name == "nt":
                self.library_handle = cdll.LoadLibrary(find_file_in_path("G2.dll"))
            else:
                self.library_handle = cdll.LoadLibrary("libG2.so")
        except OSError as err:
            # TODO: Change to Sz library when the libG2.so is changed in a build
            raise SzError("Failed to load the G2 library") from err

        # Initialize C function input parameters and results
        # Must be synchronized with g2/sdk/c/libg2product.h

        self.library_handle.G2Product_destroy.argtypes = []
        self.library_handle.G2Product_destroy.restype = c_longlong
        self.library_handle.G2Product_init.argtypes = [c_char_p, c_char_p, c_int]
        self.library_handle.G2Product_init.restype = c_longlong
        self.library_handle.G2Product_license.argtypes = []
        self.library_handle.G2Product_license.restype = c_char_p
        self.library_handle.G2Product_version.argtypes = []
        self.library_handle.G2Product_version.restype = c_char_p
        self.library_handle.G2GoHelper_free.argtypes = [c_char_p]

        # Optionally, initialize Senzing engine.

        if (len(self.instance_name) == 0) or (len(self.settings) == 0):
            if len(self.instance_name) + len(self.settings) != 0:
                raise self.new_exception(4003)
        if len(instance_name) > 0:
            self.auto_init = True
            self.initialize(self.instance_name, self.settings, self.verbose_logging)

    def __del__(self) -> None:
        """Destructor"""
        if self.auto_init:
            try:
                self.destroy()
            except SzError:
                pass

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
    # Exception helpers
    # -------------------------------------------------------------------------

    def new_exception(self, error_id: int) -> Exception:
        """
        Generate a new exception based on the error_id.

        :meta private:
        """
        return new_szexception(
            self.library_handle.G2Product_getLastException,
            self.library_handle.G2Product_clearLastException,
            self.library_handle.G2Product_getLastExceptionCode,
            SENZING_PRODUCT_ID,
            error_id,
        )

    # -------------------------------------------------------------------------
    # SzProduct methods
    # -------------------------------------------------------------------------

    def destroy(self, **kwargs: Any) -> None:
        result = self.library_handle.G2Product_destroy()
        if result != 0:
            raise self.new_exception(4001)

    @catch_ctypes_exceptions
    def initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        result = self.library_handle.G2Product_init(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            verbose_logging,
        )
        if result < 0:
            raise self.new_exception(4002)

    def get_license(self, **kwargs: Any) -> str:
        return as_python_str(self.library_handle.G2Product_license())

    def get_version(self, **kwargs: Any) -> str:
        return as_python_str(self.library_handle.G2Product_version())
