try:
    import json

    from ._helpers import is_senzing_binary_version_supported
    from .szabstractfactory import (
        SzAbstractFactoryCore,
        SzAbstractFactoryParametersCore,
    )
    from .szconfig import SzConfigCore
    from .szconfigmanager import SzConfigManagerCore
    from .szdiagnostic import SzDiagnosticCore
    from .szengine import SzEngineCore
    from .szproduct import SzProductCore

    sz_product = SzProductCore()
    sz_product._initialize("sdk_init_check", "{}")
    version: str = json.loads(sz_product.get_version()).get("VERSION", "0.0.0")
    is_senzing_binary_version_supported(version)
except (ImportError, SyntaxError) as err:
    import sys

    if sys.version_info < (3, 9):
        from senzing import SzSdkError

        SYS_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
        raise SzSdkError(f"Current Python version {SYS_VERSION} doesn't meet the minimum requirement of 3.9") from err
    raise err
finally:
    if "sz_product" in locals():
        sz_product._destroy()

__all__ = [
    "SzAbstractFactoryCore",
    "SzAbstractFactoryParametersCore",
    "SzConfigCore",
    "SzConfigManagerCore",
    "SzDiagnosticCore",
    "SzEngineCore",
    "SzProductCore",
]
