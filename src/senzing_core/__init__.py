# TODO -
try:
    # from ._version import get_senzingsdk_version, is_supported_senzingsdk_version
    from _helpers import is_senzing_binary_version_supported

    from ._version import get_senzingsdk_version

    is_senzing_binary_version_supported(get_senzingsdk_version())
    # is_senzing_binary_version_supported("3.9.9")

    from .szabstractfactory import (
        SzAbstractFactoryCore,
        SzAbstractFactoryParametersCore,
    )
    from .szconfig import SzConfigCore
    from .szconfigmanager import SzConfigManagerCore
    from .szdiagnostic import SzDiagnosticCore
    from .szengine import SzEngineCore
    from .szproduct import SzProductCore


# TODO - SyntaxError when modern Python such as walrus operator used, test for Python version...
except (ImportError, SyntaxError) as err:
    import sys

    from senzing import SzSdkError

    if sys.version_info < (3, 9):
        SYS_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
        raise SzSdkError(f"Current Python version {SYS_VERSION} doesn't meet the minimum requirement of 3.9") from err
    raise err

__all__ = [
    "SzAbstractFactoryCore",
    "SzAbstractFactoryParametersCore",
    "SzConfigCore",
    "SzConfigManagerCore",
    "SzDiagnosticCore",
    "SzEngineCore",
    "SzProductCore",
]


# TODO -
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
