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


from ctypes import c_char_p, c_int, c_longlong
from functools import partial
from typing import Any, Dict, Union

from senzing import SzProductAbstract, sdk_exception

from .szhelpers import (
    as_c_char_p,
    as_python_str,
    as_str,
    catch_ctypes_exceptions,
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

        # self.auto_init = False
        self.instance_name = instance_name
        self.settings = settings
        self.verbose_logging = verbose_logging

        # # Load binary library.

        # try:
        #     if os.name == "nt":
        #         self.library_handle = cdll.LoadLibrary(find_file_in_path("G2.dll"))
        #     else:
        #         self.library_handle = cdll.LoadLibrary("libG2.so")
        # except OSError as err:
        #     # TODO: Change to Sz library when the libG2.so is changed in a build
        #     # raise SzError("Failed to load the G2 library") from err
        #     print(
        #         "ERROR: Unable to load G2. Did you remember to setup your environment by sourcing the setupEnv file?"
        #     )
        #     print(
        #         "ERROR: For more information see https://senzing.zendesk.com/hc/en-us/articles/115002408867-Introduction-G2-Quickstart"
        #     )
        #     print(
        #         "ERROR: If you are running Ubuntu or Debian please also review the ssl and crypto information at https://senzing.zendesk.com/hc/en-us/articles/115010259947-System-Requirements"
        #     )
        #     # raise sdk_exception(1) from err
        #     raise sdk_exception(1) from err

        # Load binary library.
        self.library_handle = load_sz_library()

        # Partial function to use this modules self.library_handle for exception handling
        self.check_result = partial(
            check_result_rc,
            self.library_handle.G2Product_getLastException,
            self.library_handle.G2Product_clearLastException,
            self.library_handle.G2Product_getLastExceptionCode,
            # SENZING_PRODUCT_ID,
        )

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

        # if (len(self.instance_name) == 0) or (len(self.settings) == 0):
        #     if len(self.instance_name) + len(self.settings) != 0:
        #         raise sdk_exception(SENZING_PRODUCT_ID, 4001, 1)
        # if len(instance_name) > 0:
        #     self.auto_init = True

        # NOTE both get_license and get_version will work if "", "{}" are passed in
        if not self.instance_name or len(self.settings) == 0:
            # raise sdk_exception(SENZING_PRODUCT_ID, 4001, 1)
            raise sdk_exception(2)
        #     self._initialize("", "")

        self._initialize(self.instance_name, self.settings, self.verbose_logging)

    def __del__(self) -> None:
        """Destructor"""
        # if self.auto_init:
        # with suppress(SzError):
        #     self._destroy()
        # NOTE This is to catch the G2 library not being available (AttributeError)
        # NOTE and prevent 'Exception ignored in:' messages __del__ can produce
        # NOTE https://docs.python.org/3/reference/datamodel.html#object.__del__
        try:
            self._destroy()
        except AttributeError:
            return None

    # -------------------------------------------------------------------------
    # SzProduct methods
    # -------------------------------------------------------------------------

    # Private method
    def _destroy(self, **kwargs: Any) -> None:
        result = self.library_handle.G2Product_destroy()
        self.check_result(result)

    # Private method
    @catch_ctypes_exceptions
    def _initialize(
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
        self.check_result(result)

    def get_license(self, **kwargs: Any) -> str:
        return as_python_str(self.library_handle.G2Product_license())

    def get_version(self, **kwargs: Any) -> str:
        return as_python_str(self.library_handle.G2Product_version())
