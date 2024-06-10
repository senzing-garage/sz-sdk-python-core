# TODO: Move in szhelpers?
# TODO AC - tried to move to helpers, got circular import issues
"""
TODO: szversion.py
"""

import datetime
import json
import traceback

from senzing import SzError

from .szproduct import SzProduct

SENZING_VERSION_MINIMUM = "3.8.0"
SENZING_VERSION_MAXIMUM = "5.0.0"


def get_location() -> str:
    """
    Determine caller.

    :meta private:
    """
    stack = traceback.format_stack()
    return stack[0].replace("\n   ", "", 1).rstrip()


def normalize_semantic_version(semantic_version: str) -> int:
    """
    From a semantic version string (e.g. "M.m.P")
    create an integer for comparison.

    Note:  The current implementation supports up to 2 digit
    Major, Minor, and Patch integers. (see 10**4, 10**2)

    Args:
        semantic_version (str): A string in the form 'M.m.P'

    Returns:
        int: An integer representation of the Semantic Version string. Suitable for comparison.

    :meta private:
    """

    semantic_version_splits = semantic_version.split(".")
    result = (
        (int(semantic_version_splits[0]) * 10**4)
        + (int(semantic_version_splits[1]) * 10**2)
        + (int(semantic_version_splits[2]))
    )
    return result


def supports_senzingapi_version(
    min_semantic_version: str, max_semantic_version: str, current_semantic_version: str
) -> bool:
    """
    Determine if current semantic version string is between min and max semantic version strings.

    Args:
        min_semantic_version (str): String in form 'M.m.P' representing lowest version supported.
        max_semantic_version (str): String in form 'M.m.P' representing the version where support stops.
        current_semantic_version (str): String in form 'M.m.P' representing current version.

    Raises:
        SzError: Current Senzing API is not supported.

    Returns:
        bool: Returns True if current Senzing API version is supported.

    :meta private:
    """
    min_version = normalize_semantic_version(min_semantic_version)
    max_version = normalize_semantic_version(max_semantic_version)
    current_version = normalize_semantic_version(current_semantic_version)

    # TODO Simplify message and use sdk_exception
    if (current_version < min_version) or (current_version >= max_version):
        message = {
            "time": datetime.datetime.utcnow().isoformat("T"),
            "text": f"Current Senzing API version of {current_semantic_version} not in range {min_semantic_version} <= version < {max_semantic_version}.",
            "level": "FATAL",
            "id": "senzing-50475001",
            # "location": get_location(5),
            "location": get_location(),
        }
        raise SzError(json.dumps(message))
    return True


def is_supported_senzingapi_version() -> bool:
    """
    Determine if the Senzing API binary is supported by this
    version of the Senzing Python SDK.

    Raises:
        SzError: Current Senzing API is not supported.

    Returns:
        bool: Returns True if current Senzing API version is supported.

    :meta private:
    """

    sz_product = SzProduct("szversion", "{}")
    version_dict = json.loads(sz_product.get_version())
    senzing_version_current = version_dict.get("VERSION", "0.0.0")

    result = supports_senzingapi_version(
        SENZING_VERSION_MINIMUM, SENZING_VERSION_MAXIMUM, senzing_version_current
    )

    return result
