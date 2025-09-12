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
    check_is_destroyed,
    check_result_rc,
    load_sz_library,
)

# Metadata

__all__ = ["SzProductCore"]
__updated__ = "2025-08-06"


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
    # Dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(self, **kwargs: Any) -> None:
        _ = kwargs

        self._is_destroyed = False
        self._library_handle = load_sz_library()

        # Partial function to use this modules self._library_handle for exception handling
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
        self._library_handle.SzProduct_getLicense.argtypes = []
        self._library_handle.SzProduct_getLicense.restype = c_char_p
        self._library_handle.SzProduct_getVersion.argtypes = []
        self._library_handle.SzProduct_getVersion.restype = c_char_p
        self._library_handle.SzProduct_init.argtypes = [c_char_p, c_char_p, c_int]
        self._library_handle.SzProduct_init.restype = c_longlong
        self._library_handle.SzHelper_free.argtypes = [c_void_p]

    @property
    def is_destroyed(self) -> bool:
        """Return if the instance has been destroyed."""
        return self._is_destroyed

    # -------------------------------------------------------------------------
    # SzProduct methods
    # -------------------------------------------------------------------------

    # NOTE - Not to use check_is_destroyed decorator
    def _destroy(self) -> None:
        if not self._is_destroyed:
            _ = self._library_handle.SzProduct_destroy()
            self._is_destroyed = True

    # NOTE - Internal use only!
    def _internal_only_destroy(self) -> None:
        result = self._library_handle.SzProduct_destroy()
        self._check_result(result)

    @check_is_destroyed
    @catch_sdk_exceptions
    def _initialize(
        self,
        instance_name: str,
        settings: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
    ) -> None:
        result = self._library_handle.SzProduct_init(
            as_c_char_p(instance_name),
            as_c_char_p(as_str(settings)),
            verbose_logging,
        )
        self._check_result(result)

    @check_is_destroyed
    def get_license(self) -> str:
        return as_python_str(self._library_handle.SzProduct_getLicense())

    @check_is_destroyed
    def get_version(self) -> str:
        return as_python_str(self._library_handle.SzProduct_getVersion())
