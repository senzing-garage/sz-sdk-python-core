"""
``senzing_core.szproduct.SzProductCore`` is an implementation
of the `senzing.szproduct.SzProduct`_ interface that communicates with the Senzing binaries.

To use szproduct,
the **LD_LIBRARY_PATH** environment variable must include a path to Senzing's libraries.

Example:

.. code-block:: bash

    export LD_LIBRARY_PATH=/opt/senzing/er/lib

.. _senzing.szproduct.SzProduct: https://garage.senzing.com/sz-sdk-python/senzing.html#module-senzing.szproduct
"""

# pylint: disable=R0903

from ctypes import c_char_p, c_int, c_longlong, c_void_p
from functools import partial
from typing import Any, Dict, Union

from senzing import SzProduct

from ._helpers import (
    as_c_char_p,
    as_python_str,
    as_str,
    catch_sdk_exceptions,
    check_result_rc,
    is_python_version_supported,
    load_sz_library,
)

# Metadata

__all__ = ["SzProductCore"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2025-01-28"


# -----------------------------------------------------------------------------
# SzProductCore class
# -----------------------------------------------------------------------------


class SzProductCore(SzProduct):
    """
    Use SzAbstractFactoryCore.create_product() to create an SzProduct object.
    The SzProduct object uses the arguments provided to the SzAbstractFactoryCore().

    Example:

    .. code-block:: python

        from senzing_core import SzAbstractFactoryCore

        sz_abstract_factory = SzAbstractFactoryCore(instance_name, settings)
        sz_product = sz_abstract_factory.create_product()

    Args:

    Raises:

    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(self, **kwargs: Any) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """

        _ = kwargs

        is_python_version_supported()
        self._library_handle = load_sz_library()

        # Partial function to use this modules self.library_handle for exception handling
        self._check_result = partial(
            check_result_rc,
            self._library_handle.SzProduct_getLastException,
            self._library_handle.SzProduct_clearLastException,
            self._library_handle.SzProduct_getLastExceptionCode,
        )

        # Initialize C function input parameters and results
        # Must be synchronized with /opt/senzing/er/sdk/c/libSzProduct.h

        self._library_handle.SzProduct_destroy.argtypes = []
        self._library_handle.SzProduct_destroy.restype = c_longlong
        self._library_handle.SzProduct_init.argtypes = [c_char_p, c_char_p, c_int]
        self._library_handle.SzProduct_init.restype = c_longlong
        self._library_handle.SzProduct_license.argtypes = []
        self._library_handle.SzProduct_license.restype = c_char_p
        self._library_handle.SzProduct_version.argtypes = []
        self._library_handle.SzProduct_version.restype = c_char_p
        self._library_handle.SzHelper_free.argtypes = [c_void_p]

    def __del__(self) -> None:
        """Destructor"""

    # -------------------------------------------------------------------------
    # SzProduct methods
    # -------------------------------------------------------------------------

    def _destroy(self) -> None:
        _ = self._library_handle.SzProduct_destroy()

    @catch_sdk_exceptions
    def initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
    ) -> None:
        """
        Initialize the C-based Senzing SzProduct.

        Args:
            instance_name (str): A name to distinguish this instance of the SzProduct.
            settings (Union[str, Dict[Any, Any]]): A JSON document defining runtime configuration.
            verbose_logging (int, optional): Send debug statements to STDOUT. Defaults to 0.
        """
        result = self._library_handle.SzProduct_init(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            verbose_logging,
        )
        self._check_result(result)

    def get_license(self) -> str:
        return as_python_str(self._library_handle.SzProduct_license())

    def get_version(
        self,
    ) -> str:
        return as_python_str(self._library_handle.SzProduct_version())
