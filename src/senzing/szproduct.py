"""
The `szproduct` package is used to inspect the Senzing product.
It is a wrapper over Senzing's SzProduct C binding.
It conforms to the interface specified in
`szproduct_abstract.py <https://github.com/senzing-garage/sz-sdk-python/blob/main/src/senzing_abstract/szproduct_abstract.py>`_

To use szproduct,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/er/lib
"""

# pylint: disable=R0903

from ctypes import c_char_p, c_int, c_longlong, c_void_p
from functools import partial
from typing import Any, Dict, Union

from senzing_abstract import SzProductAbstract

from ._helpers import (
    as_c_char_p,
    as_python_str,
    as_str,
    catch_exceptions,
    check_result_rc,
    load_sz_library,
)

# Metadata

__all__ = ["SzProduct"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-07"

# SENZING_PRODUCT_ID = "5046"  # See https://github.com/senzing-garage/knowledge-base/blob/main/lists/senzing-component-ids.md

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

    # TODO: Consider making usual constructor private (`SzConfig.SzConfig()`)
    # and replacing it with static constructor (i.e. `SzConfig.NewABC(str,str)`, `SzConfig.NewDEF(str,dict))

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        # TODO
        # instance_name: str = "",
        # settings: Union[str, Dict[Any, Any]] = "",
        # settings: Union[str, Dict[Any, Any]] = "{}",
        # verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """

        # self.initialized = False
        # self.instance_name = instance_name
        # self.settings = settings
        # self.verbose_logging = verbose_logging

        # Load binary library.
        self.library_handle = load_sz_library()

        # Partial function to use this modules self.library_handle for exception handling
        self.check_result = partial(
            check_result_rc,
            self.library_handle.SzProduct_getLastException,
            self.library_handle.SzProduct_clearLastException,
            self.library_handle.SzProduct_getLastExceptionCode,
        )

        # Initialize C function input parameters and results
        # Must be synchronized with /opt/senzing/er/sdk/c/libSzProduct.h

        self.library_handle.SzProduct_destroy.argtypes = []
        self.library_handle.SzProduct_destroy.restype = c_longlong
        self.library_handle.SzProduct_init.argtypes = [c_char_p, c_char_p, c_int]
        self.library_handle.SzProduct_init.restype = c_longlong
        self.library_handle.SzProduct_license.argtypes = []
        self.library_handle.SzProduct_license.restype = c_char_p
        self.library_handle.SzProduct_version.argtypes = []
        self.library_handle.SzProduct_version.restype = c_char_p
        self.library_handle.SzHelper_free.argtypes = [c_void_p]

        # NOTE both get_license and get_version will work if "", "{}" are passed in
        # TODO
        # if not self.instance_name or len(self.settings) == 0:
        #     raise sdk_exception(2)

        # Initialize Senzing engine.
        # self._initialize(self.instance_name, self.settings, self.verbose_logging)
        # self.initialized = True

    def __del__(self) -> None:
        """Destructor"""
        # if self.initialized:
        #     with suppress(Exception):
        #         self._destroy()

    # -------------------------------------------------------------------------
    # SzProduct methods
    # -------------------------------------------------------------------------

    def _destroy(self, **kwargs: Any) -> None:
        _ = self.library_handle.SzProduct_destroy()

    @catch_exceptions
    def _initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        result = self.library_handle.SzProduct_init(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            verbose_logging,
        )
        self.check_result(result)

    def get_license(self, **kwargs: Any) -> str:
        return as_python_str(self.library_handle.SzProduct_license())

    def get_version(self, **kwargs: Any) -> str:
        return as_python_str(self.library_handle.SzProduct_version())
