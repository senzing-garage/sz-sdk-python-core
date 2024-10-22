#! /usr/bin/env python3

"""
TODO: szabstractfactory.py
"""

# pylint: disable=E1101

from types import TracebackType
from typing import Any, Dict, Type, Union

from senzing_abstract import (
    SzAbstractFactoryAbstract,
    SzConfigAbstract,
    SzConfigManagerAbstract,
    SzDiagnosticAbstract,
    SzEngineAbstract,
    SzProductAbstract,
)

from .szconfig import SzConfig
from .szconfigmanager import SzConfigManager
from .szdiagnostic import SzDiagnostic
from .szengine import SzEngine
from .szproduct import SzProduct

# Metadata

__all__ = ["SzAbstractFactoryAbstract"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2024-10-21"
__updated__ = "2024-10-24"


# -----------------------------------------------------------------------------
# SzAbstractFactory class
# -----------------------------------------------------------------------------


class SzAbstractFactory(SzAbstractFactoryAbstract):
    """
    SzAbstractFactory module is a factory pattern for accessing Senzing over gRPC.
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
        **kwargs: Any,
    ) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """
        self.instance_name = instance_name
        self.settings = settings
        self.config_id = config_id
        self.verbose_logging = verbose_logging
        self.is_szconfig_initialized = False
        self.is_szconfigmanager_initialized = False
        self.is_szdiagnostic_initialized = False
        self.is_szengine_initialized = False
        self.is_szproduct_initialized = False

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
        if not self.is_szengine_initialized or not self.is_szdiagnostic_initialized:
            # TODO: destroy  (Ant, can you see what's wrong with destroying Senzing process?  Hint: scope)
            pass

    # -------------------------------------------------------------------------
    # SzAbstractFactory methods
    # -------------------------------------------------------------------------

    def create_sz_config(self, **kwargs: Any) -> SzConfigAbstract:
        # TODO: Do parameters need to be passed in?
        result = SzConfig()
        if not self.is_szconfig_initialized:
            result._initialize(  # pylint: disable=W0212
                instance_name=self.instance_name,
                settings=self.settings,
                verbose_logging=self.verbose_logging,
            )
            self.is_szconfig_initialized = True
        return result

    def create_sz_configmanager(self, **kwargs: Any) -> SzConfigManagerAbstract:
        result = SzConfigManager()
        if not self.is_szconfigmanager_initialized:
            result._initialize(  # pylint: disable=W0212
                instance_name=self.instance_name,
                settings=self.settings,
                verbose_logging=self.verbose_logging,
            )
            self.is_szconfigmanager_initialized = True
        return result

    def create_sz_diagnostic(self, **kwargs: Any) -> SzDiagnosticAbstract:
        result = SzDiagnostic()
        if not self.is_szdiagnostic_initialized:
            result._initialize(  # pylint: disable=W0212
                instance_name=self.instance_name,
                settings=self.settings,
                verbose_logging=self.verbose_logging,
            )
            self.is_szdiagnostic_initialized = True
        return result

    def create_sz_engine(self, **kwargs: Any) -> SzEngineAbstract:
        # TODO: Determine if atomic is needed.
        result = SzEngine()
        if not self.is_szengine_initialized:
            result._initialize(  # pylint: disable=W0212
                instance_name=self.instance_name,
                settings=self.settings,
                config_id=self.config_id,
                verbose_logging=self.verbose_logging,
            )
            self.is_szengine_initialized = True
        return result

    def create_sz_product(self, **kwargs: Any) -> SzProductAbstract:
        result = SzProduct()
        if not self.is_szproduct_initialized:
            result._initialize(  # pylint: disable=W0212
                instance_name=self.instance_name,
                settings=self.settings,
                verbose_logging=self.verbose_logging,
            )
            self.is_szproduct_initialized = True
        return result

    def destroy(self, **kwargs: Any) -> None:
        # TODO: Implement function.
        # TODO: Determine if atomic

        # if not self.is_szengine_initialized:
        #     xxx
        #     sz_engine = self.create_sz_engine()
        #     sz_engine._destroy()
        #     self.is_szengine_initialized = False

        pass

    def reinitialize(self, config_id: int = 0, **kwargs: Any) -> None:
        # TODO: Implement function.
        # TODO: Determine if atomic

        _ = config_id
