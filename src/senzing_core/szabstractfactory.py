#! /usr/bin/env python3

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
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """
        self.instance_name = instance_name
        self.settings = settings
        self.config_id = config_id
        self.verbose_logging = verbose_logging
        self.is_szconfigmanager_initialized = False
        self.is_szdiagnostic_initialized = False
        self.is_szengine_initialized = False
        self.is_szproduct_initialized = False

    def __enter__(
        self,
    ) -> Any:
        """Context Manager method."""
        return self

    def __del__(self) -> None:
        """Destructor"""
        self._destroy()

    def __exit__(
        self,
        exc_type: Union[Type[BaseException], None],
        exc_val: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ) -> None:
        """Context Manager method."""
        self._destroy()

    # -------------------------------------------------------------------------
    # SzAbstractFactory methods
    # -------------------------------------------------------------------------

    def create_configmanager(self) -> SzConfigManager:
        result = SzConfigManagerCore()
        if not self.is_szconfigmanager_initialized:
            result.initialize(  # pylint: disable=W0212
                instance_name=self.instance_name,
                settings=self.settings,
                verbose_logging=self.verbose_logging,
            )
            self.is_szconfigmanager_initialized = True
        return result

    def create_diagnostic(self) -> SzDiagnostic:
        result = SzDiagnosticCore()
        if not self.is_szdiagnostic_initialized:
            result.initialize(  # pylint: disable=W0212
                instance_name=self.instance_name,
                settings=self.settings,
                config_id=self.config_id,
                verbose_logging=self.verbose_logging,
            )
            self.is_szdiagnostic_initialized = True
        return result

    def create_engine(self) -> SzEngine:
        # TODO: Determine if atomic operation is needed.
        result = SzEngineCore()
        if not self.is_szengine_initialized:
            result.initialize(  # pylint: disable=W0212
                instance_name=self.instance_name,
                settings=self.settings,
                config_id=self.config_id,
                verbose_logging=self.verbose_logging,
            )
            self.is_szengine_initialized = True
        return result

    def create_product(self) -> SzProduct:
        result = SzProductCore()
        if not self.is_szproduct_initialized:
            result.initialize(  # pylint: disable=W0212
                instance_name=self.instance_name,
                settings=self.settings,
                verbose_logging=self.verbose_logging,
            )
            self.is_szproduct_initialized = True
        return result

    def _destroy(self) -> None:

        # TODO: Determine if atomic operation is needed.

        if self.is_szconfigmanager_initialized:
            self.is_szconfigmanager_initialized = False
            sz_configmanager = SzConfigManagerCore()
            sz_configmanager._destroy()  # pylint: disable=W0212

        if self.is_szdiagnostic_initialized:
            self.is_szdiagnostic_initialized = False
            sz_diagnostic = SzDiagnosticCore()
            sz_diagnostic._destroy()  # pylint: disable=W0212

        if self.is_szengine_initialized:
            self.is_szengine_initialized = False
            sz_engine = SzEngineCore()
            sz_engine._destroy()  # pylint: disable=W0212

        if self.is_szproduct_initialized:
            self.is_szproduct_initialized = False
            sz_product = SzProductCore()
            sz_product._destroy()  # pylint: disable=W0212

    def reinitialize(self, config_id: int) -> None:

        # TODO: Determine if atomic operation is needed.

        self.config_id = config_id

        if self.is_szengine_initialized:
            sz_engine = SzEngineCore()
            sz_engine._reinitialize(config_id=config_id)  # pylint: disable=W0212

        if self.is_szdiagnostic_initialized:
            sz_diagnostic = SzDiagnosticCore()
            sz_diagnostic._reinitialize(config_id=config_id)  # pylint: disable=W0212
        if self.is_szengine_initialized:
            sz_engine = SzEngineCore()
            sz_engine._reinitialize(config_id=config_id)  # pylint: disable=W0212

        if self.is_szdiagnostic_initialized:
            sz_diagnostic = SzDiagnosticCore()
            sz_diagnostic._reinitialize(config_id=config_id)  # pylint: disable=W0212
