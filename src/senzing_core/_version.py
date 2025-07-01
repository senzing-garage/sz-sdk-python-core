"""
Check if supported versions for the Senzing SDK binary and Python
"""

import json

from .szproduct import SzProductCore

# TODO - Clean up, rename to versions? Take back out of _helpers? If szabstract factory python check is in here use SzSDkError
# import sys
# from sys import version_info

# from senzing import SzSdkError


# PYTHON_VERSION_MINIMUM = "3.9"
# SENZING_VERSION_MINIMUM = "4.0.0"
# SENZING_VERSION_MAXIMUM = "5.0.0"


# # TODO -
def get_senzingsdk_version() -> str:
    """
    Use szproduct to return the Senzing SDK binary version.

    Raises:

    Returns:
        str: Returns the Senzing SDK binary version.

    :meta private:
    """

    sz_product = SzProductCore()
    sz_product.initialize("_version", "{}")
    version: str = json.loads(sz_product.get_version()).get("VERSION", "0.0.0")

    return version


# def normalize_semantic_version(semantic_version: str) -> int:
#     """
#     From a semantic version string (e.g. "M.m.P") create an integer for comparison.

#     Note:  The current implementation supports up to 2 digit Major, Minor, and Patch integers. (see 10**4, 10**2)
#            Either Major, Minor and Patch or Major, Minor

#     Args:
#         semantic_version (str): A string in the form 'M.m.P'

#     Returns:
#         int: An integer representation of the Semantic Version string. Suitable for comparison.

#     :meta private:
#     """
#     semantic_version_splits = semantic_version.split(".")
#     if len(semantic_version_splits) == 3:
#         result = (
#             (int(semantic_version_splits[0]) * 10**4)
#             + (int(semantic_version_splits[1]) * 10**2)
#             + (int(semantic_version_splits[2]))
#         )
#     elif len(semantic_version_splits) == 2:
#         result = (int(semantic_version_splits[0]) * 10**4) + (int(semantic_version_splits[1]) * 10**2)
#     else:
#         message = "semantic_version should either be M.m.P or M.m, e.g., 4.0.0 or 4.0"
#         raise SzSdkError(message)

#     return result


# def supports_senzingsdk_version(
#     min_semantic_version: str, max_semantic_version: str, current_semantic_version: str
# ) -> bool:
#     """
#     Determine if current semantic version string is between min and max semantic version strings.

#     Args:
#         min_semantic_version (str): String in form 'M.m.P' representing lowest version supported.
#         max_semantic_version (str): String in form 'M.m.P' representing the version where support stops.
#         current_semantic_version (str): String in form 'M.m.P' representing current version.

#     Raises:
#         SzSdkError: Current Senzing SDK is not supported.

#     Returns:
#         bool: Returns True if current Senzing SDK binary version is supported.

#     :meta private:
#     """
#     min_version = normalize_semantic_version(min_semantic_version)
#     max_version = normalize_semantic_version(max_semantic_version)
#     current_version = normalize_semantic_version(current_semantic_version)

#     if (current_version < min_version) or (current_version >= max_version):
#         message = f"Current Senzing SDK binary version of {current_semantic_version} not in range {min_semantic_version} <= version < {max_semantic_version}."
#         raise SzSdkError(message)
#     return True


# # TODO -
# def is_senzing_binary_version_supported(
#     # TODO -
#     # min_semantic_version: str, max_semantic_version: str, current_semantic_version: str
#     current_semantic_version: str,
#     min_semantic_version: str = SENZING_VERSION_MINIMUM,
#     max_semantic_version: str = SENZING_VERSION_MAXIMUM,
# ) -> bool:
#     """
#     Determine if the Senzing SDK binary is supported by this version of the Senzing Python SDK.

#     Args:
#         min_semantic_version (str): String in form 'M.m.P' representing lowest version supported.
#         max_semantic_version (str): String in form 'M.m.P' representing the version where support stops.
#         current_semantic_version (str): String in form 'M.m.P' representing current version.

#     Raises:
#         SzSdkError: Current Senzing SDK is not supported.

#     Returns:
#         bool: Returns True if current Senzing SDK binary version is supported.

#     :meta private:
#     """
#     min_version = normalize_semantic_version(min_semantic_version)
#     max_version = normalize_semantic_version(max_semantic_version)
#     current_version = normalize_semantic_version(current_semantic_version)

#     if (current_version < min_version) or (current_version >= max_version):
#         message = f"Current Senzing SDK binary version of {current_semantic_version} not in range {min_semantic_version} <= version < {max_semantic_version}."
#         raise SzSdkError(message)

#     return True


# def is_supported_senzingsdk_version() -> bool:
#     """
#     Determine if the Senzing SDK binary is supported by this version of the Senzing Python SDK.

#     Raises:
#         SzSdkError: Current Senzing SDK is not supported.

#     Returns:
#         bool: Returns True if current Senzing SDK binary version is supported.

#     :meta private:
#     """
#     sz_product = SzProductCore()
#     sz_product.initialize("_version", "{}")  # pylint: disable=W0212
#     version_dict = json.loads(sz_product.get_version())
#     senzing_version_current = version_dict.get("VERSION", "0.0.0")
#     result = supports_senzingsdk_version(SENZING_VERSION_MINIMUM, SENZING_VERSION_MAXIMUM, senzing_version_current)

#     return result


# def is_supported_python_version(min_version: str = PYTHON_VERSION_MINIMUM) -> bool:
#     """
#     Determine if the minimum Python version is supported.

#     Raises:
#         SzSdkError: Current Python version is not supported.

#     Returns:
#         bool: Returns True if current Python version is supported.

#     :meta private:
#     """
#     min_version_normalized = normalize_semantic_version(min_version)
#     runtime_version = f"{version_info.major}.{version_info.minor}"
#     runtime_version_normalized = normalize_semantic_version(runtime_version)

#     if runtime_version_normalized < min_version_normalized:
#         message = f"Current Python version of {runtime_version} doesn't meet minimum requirement of {min_version}"
#         raise SzSdkError(message)

#     return True


# def check_requirements(min_python_version: str = PYTHON_VERSION_MINIMUM) -> bool:
#     """
#     Determine if the minimum Python and Senzing SDK binary versions are supported.

#     Raises:
#         SzSdkError: One or both versions are not supported.

#     Returns:
#         bool: Returns True if Python and Senzing SDK binary versions are supported.

#     :meta private:
#     """
#     return all((is_supported_python_version(min_python_version), is_supported_senzingsdk_version()))
