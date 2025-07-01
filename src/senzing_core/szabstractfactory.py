"""
``senzing_core.szabstractfactory.SzAbstractFactoryCore`` is an implementation
of the `senzing.szabstractfactory.SzAbstractFactory`_ interface that communicates with the Senzing binaries.

.. _senzing.szabstractfactory.SzAbstractFactory: https://garage.senzing.com/sz-sdk-python/senzing.html#module-senzing.szabstractfactory
"""

# pylint: disable=E1101

from types import TracebackType
from typing import Any, Dict, Type, TypedDict, Union

from senzing import (
    SzAbstractFactory,
    SzConfigManager,
    SzDiagnostic,
    SzEngine,
    SzProduct,
)

from .szconfigmanager import SzConfigManagerCore
from .szdiagnostic import SzDiagnosticCore
from .szengine import SzEngineCore
from .szproduct import SzProductCore

# # TODO -
# try:
#     # from ._helpers import get_senzingsdk_version, is_senzing_binary_version_supported
#     # is_senzing_binary_version_supported(get_senzingsdk_version())
#     from typing import Any, Dict, Type, TypedDict, Union

#     from ._version import is_supported_senzingsdk_version

# except (ImportError, SyntaxError) as err:
#     import sys

#     from senzing import SzSdkError

#     if sys.version_info < (3, 9):
#         SYS_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
#         raise SzSdkError(f"Current Python version {SYS_VERSION} doesn't meet the minimum requirement of 3.9") from err
#     raise err


# Metadata

__all__ = ["SzAbstractFactoryCore", "SzAbstractFactoryParametersCore"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2024-10-21"
__updated__ = "2025-01-28"


# -----------------------------------------------------------------------------
# SzAbstractFactoryParametersCore class
# -----------------------------------------------------------------------------


class SzAbstractFactoryParametersCore(TypedDict, total=False):
    """
    SzAbstractFactoryParametersCore is used to create a dictionary that can be unpacked when creating an
    SzAbstractFactory.
    """

    instance_name: str
    settings: Union[str, Dict[Any, Any]]
    config_id: int
    verbose_logging: int


# -----------------------------------------------------------------------------
# SzAbstractFactoryCore class
# -----------------------------------------------------------------------------


class SzAbstractFactoryCore(SzAbstractFactory):
    """
    SzAbstractFactoryCore is a factory pattern for accessing Senzing.
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        instance_name: str = "",
        settings: Union[str, Dict[Any, Any]] = "",
        config_id: int = 0,
        verbose_logging: int = 0,
    ) -> None:
        """
        Initializer.

        Args:
            instance_name (str): A name to distinguish the instances of engine objects.
            settings (Union[str, Dict[Any, Any]]): A JSON document defining runtime configuration.
            config_id (int, optional): Initialize with a specific configuration ID. Defaults to 0 which uses the current system DEFAULTCONFIGID.
            verbose_logging (int, optional): Send debug statements to STDOUT. Defaults to 0.
        """
        self._instance_name = instance_name
        self._settings = settings
        self._config_id = config_id
        self._verbose_logging = verbose_logging
        self._is_szconfigmanager_initialized = False
        self._is_szdiagnostic_initialized = False
        self._is_szengine_initialized = False
        self._is_szproduct_initialized = False

    def __enter__(
        self,
    ) -> Any:
        """Context Manager method."""
        return self

    # TODO -
    # def __del__(self) -> None:
    #     """Destructor"""
    #     self._destroy()

    def __exit__(
        self,
        exc_type: Union[Type[BaseException], None],
        exc_val: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ) -> None:
        """Context Manager method."""
        self._destroy()

    @property
    def instance_name(self) -> str:
        """Get the instance name the abstract factory was instantiated with."""
        return self._instance_name

    @property
    def settings(self) -> Union[str, Dict[Any, Any]]:
        """Get the settings the abstract factory was instantiated with."""
        return self._settings

    @property
    def config_id(self) -> int:
        """Get the config ID the abstract factory was instantiated with. If this is 0 no config ID was specified and
        the current system DEFAULTCONFIGID was used."""
        return self._config_id

    @property
    def verbose_logging(self) -> int:
        """Get the verbose logging value the abstract factory was instantiated with."""
        return self._verbose_logging

    # -------------------------------------------------------------------------
    # SzAbstractFactory methods
    # -------------------------------------------------------------------------

    def create_configmanager(self) -> SzConfigManager:
        result = SzConfigManagerCore()
        if not self._is_szconfigmanager_initialized:
            # TODO - disable needed?
            result.initialize(  # pylint: disable=W0212
                instance_name=self._instance_name,
                settings=self._settings,
                verbose_logging=self._verbose_logging,
            )
            self._is_szconfigmanager_initialized = True
        return result

    def create_diagnostic(self) -> SzDiagnostic:
        result = SzDiagnosticCore()
        if not self._is_szdiagnostic_initialized:
            result.initialize(  # pylint: disable=W0212
                instance_name=self._instance_name,
                settings=self._settings,
                config_id=self._config_id,
                verbose_logging=self._verbose_logging,
            )
            self._is_szdiagnostic_initialized = True
        return result

    def create_engine(self) -> SzEngine:
        result = SzEngineCore()
        if not self._is_szengine_initialized:
            result.initialize(  # pylint: disable=W0212
                instance_name=self._instance_name,
                settings=self._settings,
                config_id=self._config_id,
                verbose_logging=self._verbose_logging,
            )
            self._is_szengine_initialized = True
        return result

    def create_product(self) -> SzProduct:
        result = SzProductCore()
        if not self._is_szproduct_initialized:
            result.initialize(  # pylint: disable=W0212
                instance_name=self._instance_name,
                settings=self._settings,
                verbose_logging=self._verbose_logging,
            )
            self._is_szproduct_initialized = True
        return result

    def _destroy(self) -> None:
        if self._is_szconfigmanager_initialized:
            self._is_szconfigmanager_initialized = False
            sz_configmanager = SzConfigManagerCore()
            sz_configmanager._destroy()  # pylint: disable=W0212

        if self._is_szdiagnostic_initialized:
            self._is_szdiagnostic_initialized = False
            sz_diagnostic = SzDiagnosticCore()
            sz_diagnostic._destroy()  # pylint: disable=W0212

        if self._is_szengine_initialized:
            self._is_szengine_initialized = False
            sz_engine = SzEngineCore()
            sz_engine._destroy()  # pylint: disable=W0212

        if self._is_szproduct_initialized:
            self._is_szproduct_initialized = False
            sz_product = SzProductCore()
            sz_product._destroy()  # pylint: disable=W0212

    def reinitialize(self, config_id: int) -> None:
        self._config_id = config_id

        if self._is_szengine_initialized:
            sz_engine = SzEngineCore()
            sz_engine.reinitialize(config_id=config_id)  # pylint: disable=W0212

        if self._is_szdiagnostic_initialized:
            sz_diagnostic = SzDiagnosticCore()
            sz_diagnostic.reinitialize(config_id=config_id)  # pylint: disable=W0212
