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
    catch_non_sz_exceptions,
    check_result_rc,
    load_sz_library,
)

# Metadata

__all__ = ["SzProduct"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-11-07"


# -----------------------------------------------------------------------------
# SzProduct class
# -----------------------------------------------------------------------------


class SzProduct(SzProductAbstract):
    """
    Use SzAbstractFactory.create_product() to create an SzProduct object.
    The SzProduct object uses the parameters provided to the SzAbstractFactory()
    function.

    Example:

    .. code-block:: python

        sz_abstract_factory = SzAbstractFactory(instance_name, settings)
        sz_product = sz_abstract_factory.create_product()

    Parameters:

    Raises:

    """

    # TODO: Consider making usual constructor private (`SzConfig.SzConfig()`)
    # and replacing it with static constructor (i.e. `SzConfig.NewABC(str,str)`, `SzConfig.NewDEF(str,dict))

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(self, **kwargs: Any) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """

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

    def __del__(self) -> None:
        """Destructor"""

    # -------------------------------------------------------------------------
    # SzProduct methods
    # -------------------------------------------------------------------------

    def _destroy(self) -> None:
        _ = self.library_handle.SzProduct_destroy()

    @catch_non_sz_exceptions
    def _initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
    ) -> None:
        result = self.library_handle.SzProduct_init(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            verbose_logging,
        )
        self.check_result(result)

    def get_license(self) -> str:
        return as_python_str(self.library_handle.SzProduct_license())

    def get_version(
        self,
    ) -> str:
        return as_python_str(self.library_handle.SzProduct_version())
