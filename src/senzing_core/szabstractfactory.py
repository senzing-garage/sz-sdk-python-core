"""
``senzing_core.szabstractfactory.SzAbstractFactoryCore`` is an implementation
of the `senzing.szabstractfactory.SzAbstractFactory`_ interface that communicates with the Senzing binaries.

.. _senzing.szabstractfactory.SzAbstractFactory: https://garage.senzing.com/sz-sdk-python/senzing.html#module-senzing.szabstractfactory
"""

# pylint: disable=E1101

from __future__ import annotations

import functools
import weakref
from collections.abc import Iterable
from contextlib import suppress
from threading import Lock
from typing import Any, Callable, TypedDict, TypeVar, cast

from senzing import (
    SzAbstractFactory,
    SzConfigManager,
    SzDiagnostic,
    SzEngine,
    SzProduct,
    SzSdkError,
)

from .szconfigmanager import SzConfigManagerCore
from .szdiagnostic import SzDiagnosticCore
from .szengine import SzEngineCore
from .szproduct import SzProductCore

_WrappedFunc = TypeVar("_WrappedFunc", bound=Callable[..., Any])


# Metadata

__all__ = ["SzAbstractFactoryCore", "SzAbstractFactoryParametersCore"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2024-10-21"
__updated__ = "2025-01-28"


# -----------------------------------------------------------------------------
# Decorators
# -----------------------------------------------------------------------------


def _check_is_destroyed(func: _WrappedFunc) -> _WrappedFunc:
    """Check if the instance has been destroyed"""

    @functools.wraps(func)
    def wrapped_check_destroyed(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        if self._is_destroyed:  # pylint: disable=protected-access
            raise SzSdkError("factory has been destroyed and can no longer be used, create a new one")
        return func(self, *args, **kwargs)

    return cast(_WrappedFunc, wrapped_check_destroyed)


def _method_lock(func: _WrappedFunc) -> _WrappedFunc:
    """Lock methods"""

    @functools.wraps(func)
    def wrapped_method_lock(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        with self._method_lock:  # pylint: disable=protected-access
            return func(self, *args, **kwargs)

    return cast(_WrappedFunc, wrapped_method_lock)


# -----------------------------------------------------------------------------
# SzAbstractFactoryParametersCore class
# -----------------------------------------------------------------------------


class SzAbstractFactoryParametersCore(TypedDict, total=False):
    """Used to create a dictionary that can be unpacked when creating an SzAbstractFactory."""

    instance_name: str
    settings: str | dict[Any, Any]
    config_id: int
    verbose_logging: int


# -----------------------------------------------------------------------------
# SzAbstractFactoryCore class
# -----------------------------------------------------------------------------


class SzAbstractFactoryCore(SzAbstractFactory):
    """SzAbstractFactoryCore is a factory pattern for accessing Senzing."""

    _constructor_lock = Lock()
    _engine_instances = weakref.WeakValueDictionary()  # type: ignore[var-annotated]
    _factory_instances = weakref.WeakValueDictionary()  # type: ignore[var-annotated]

    def __new__(
        cls,
        instance_name: str = "",
        settings: str | dict[Any, Any] = "",
        config_id: int = 0,
        verbose_logging: int = 0,
    ) -> SzAbstractFactoryCore:

        with cls._constructor_lock:
            args_hash = cls._create_args_hash((instance_name, settings, config_id, verbose_logging))
            instance = super().__new__(cls)
            instance._args_hash = args_hash  # type: ignore[attr-defined]

            if cls not in cls._factory_instances.keys():
                cls._factory_instances[cls] = instance
            else:
                if args_hash == cls._factory_instances[cls]._args_hash:
                    instance = cls._factory_instances[cls]

                if args_hash != cls._factory_instances[cls]._args_hash:
                    raise SzSdkError(
                        "an instance currently exists with different arguments, to use new arguments destroy or delete the existing instance first (NOTE: This will destroy Senzing objects created by the current instance!)"
                    )

        return instance

    def __init__(
        self,
        instance_name: str = "",
        settings: str | dict[Any, Any] = "",
        config_id: int = 0,
        verbose_logging: int = 0,
    ) -> None:
        """
        Args:
            instance_name (str): A name to distinguish the instances of engine objects.
            settings (Union[str, Dict[Any, Any]]): A JSON document defining runtime configuration.
            config_id (int, optional): Initialize with a specific configuration ID. Defaults to 0 which uses the current system DEFAULTCONFIGID.
            verbose_logging (int, optional): Send debug statements to STDOUT. Defaults to 0.
        """
        self._config_id = config_id
        self._finalizer = weakref.finalize(self, self._do_destroy)
        self._instance_name = instance_name
        self._is_destroyed = False
        self._method_lock = Lock()
        self._settings = settings
        self._verbose_logging = verbose_logging

    @property
    def instance_name(self) -> str:
        """Return the instance name the abstract factory was instantiated with."""
        return self._instance_name

    @property
    def is_destroyed(self) -> bool:
        """Return if the instance has been destroyed."""
        return self._is_destroyed

    @property
    def settings(self) -> str | dict[Any, Any]:
        """Return the settings the abstract factory was instantiated with."""
        return self._settings

    @property
    def config_id(self) -> int:
        """Return the config ID the abstract factory was instantiated with. If this is 0 no config ID was specified and
        the current system DEFAULTCONFIGID was used."""
        return self._config_id

    @property
    def verbose_logging(self) -> int:
        """Return the verbose logging setting the abstract factory was instantiated with."""
        return self._verbose_logging

    # -------------------------------------------------------------------------
    # SzAbstractFactory methods
    # -------------------------------------------------------------------------

    @_check_is_destroyed
    @_method_lock
    def create_configmanager(self) -> SzConfigManager:
        result = SzConfigManagerCore()
        result._initialize(  # pylint: disable=protected-access
            instance_name=self._instance_name, settings=self._settings, verbose_logging=self._verbose_logging
        )
        SzAbstractFactoryCore._engine_instances[id(result)] = result
        return result

    @_check_is_destroyed
    @_method_lock
    def create_diagnostic(self) -> SzDiagnostic:
        result = SzDiagnosticCore()
        result._initialize(  # pylint: disable=protected-access
            instance_name=self._instance_name,
            settings=self._settings,
            config_id=self._config_id,
            verbose_logging=self._verbose_logging,
        )
        SzAbstractFactoryCore._engine_instances[id(result)] = result
        return result

    @_check_is_destroyed
    @_method_lock
    def create_engine(self) -> SzEngine:
        result = SzEngineCore()
        result._initialize(  # pylint: disable=protected-access
            instance_name=self._instance_name,
            settings=self._settings,
            config_id=self._config_id,
            verbose_logging=self._verbose_logging,
        )
        SzAbstractFactoryCore._engine_instances[id(result)] = result
        return result

    @_check_is_destroyed
    @_method_lock
    def create_product(self) -> SzProduct:
        result = SzProductCore()
        result._initialize(  # pylint: disable=protected-access
            instance_name=self._instance_name,
            settings=self._settings,
            verbose_logging=self._verbose_logging,
        )
        SzAbstractFactoryCore._engine_instances[id(result)] = result
        return result

    @_check_is_destroyed
    @_method_lock
    def destroy(self) -> None:
        self._finalizer()

    @staticmethod
    def _do_destroy() -> None:
        with suppress(KeyError, SzSdkError):
            for engine_object in SzAbstractFactoryCore._engine_instances.values():
                engine_object._destroy()  # pylint: disable=protected-access
                engine_object._is_destroyed = True  # pylint: disable=protected-access

        SzAbstractFactoryCore._engine_instances.clear()

        # fmt: off
        with suppress(IndexError):
            list(SzAbstractFactoryCore._factory_instances.values())[0]._is_destroyed = True  # pylint: disable=protected-access
        # fmt: on

        SzAbstractFactoryCore._factory_instances.clear()

    @_check_is_destroyed
    @_method_lock
    def reinitialize(self, config_id: int) -> None:
        self._config_id = config_id

        sz_engine = SzEngineCore()
        sz_engine._reinitialize(config_id=config_id)  # pylint: disable=protected-access

        sz_diagnostic = SzDiagnosticCore()
        sz_diagnostic._reinitialize(config_id=config_id)  # pylint: disable=protected-access

    # -------------------------------------------------------------------------
    # Utility methods
    # -------------------------------------------------------------------------

    @staticmethod
    def _create_args_hash(items_to_hash: Iterable[dict[str, str] | int | str]) -> str:
        """Create a hash of the factory initialization arguments"""
        item_strs = []

        try:
            for item in items_to_hash:
                if isinstance(item, (dict, int)):
                    item = str(item)
                item_strs.append(item.strip().replace(" ", ""))
            hash_ = str(hash("".join(item_strs)))
        except AttributeError as err:
            raise SzSdkError(f"couldn't create a hash from the factory arguments: {err}") from err

        return hash_
