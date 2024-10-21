#! /usr/bin/env python3

"""
TODO: szengineflags.py
"""

from enum import IntFlag
from typing import List, Union

from .engine_exception_map import SzError

try:
    from typing_extensions import Self  # type: ignore[attr-defined,no-redef]
except ImportError:
    from typing import Self  # type: ignore[attr-defined,no-redef]

# Metadata

__all__ = ["SzEngineFlags"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

# -----------------------------------------------------------------------------
# SzEngineFlags class
# -----------------------------------------------------------------------------


class SzEngineFlags(IntFlag):
    """Engine Flags"""

    @classmethod
    def combine_flags(cls, flags: Union[List[Self], List[str]]) -> int:
        """
        The `combine_flags` method ORs together all flags in a list of strings.

        Args:
            flags (List[str]): A list of strings each representing an engine flag.

        Returns:
            int: Value of ORing flags together.

        Raises:

        .. collapse:: Example:

            .. literalinclude:: ../../examples/misc/engine_flags_combine_flags.py
                :linenos:
                :language: python

            **Output:**

            .. literalinclude:: ../../examples/misc/engine_flags_combine_flags.txt
                :linenos:
                :language: json
        """
        result = 0
        try:
            for flag in flags:
                if isinstance(flag, str):
                    result = result | cls[flag.upper()]
                else:
                    result = result | flag
        except (AttributeError, KeyError) as err:
            raise SzError(f"{err} is not a valid engine flag") from err
        return result

    @classmethod
    # TODO - Ant - Correct type?
    def get_flag_int(cls, flag: Union[Self, str]) -> int:
        """# TODO"""
        try:
            if isinstance(flag, str):
                flag = cls[flag.upper()]
            flag_int = flag.value
        except (AttributeError, KeyError) as err:
            raise SzError(f"{err} is not a valid engine flag") from err
        return flag_int

    # Flags for exporting entity data.

    SZ_EXPORT_INCLUDE_MULTI_RECORD_ENTITIES = 1 << 0
    SZ_EXPORT_INCLUDE_POSSIBLY_SAME = 1 << 1
    SZ_EXPORT_INCLUDE_POSSIBLY_RELATED = 1 << 2
    SZ_EXPORT_INCLUDE_NAME_ONLY = 1 << 3
    SZ_EXPORT_INCLUDE_DISCLOSED = 1 << 4
    SZ_EXPORT_INCLUDE_SINGLE_RECORD_ENTITIES = 1 << 5
    SZ_EXPORT_INCLUDE_ALL_ENTITIES = (
        SZ_EXPORT_INCLUDE_MULTI_RECORD_ENTITIES
        | SZ_EXPORT_INCLUDE_SINGLE_RECORD_ENTITIES
    )
    SZ_EXPORT_INCLUDE_ALL_HAVING_RELATIONSHIPS = (
        SZ_EXPORT_INCLUDE_POSSIBLY_SAME
        | SZ_EXPORT_INCLUDE_POSSIBLY_RELATED
        | SZ_EXPORT_INCLUDE_NAME_ONLY
        | SZ_EXPORT_INCLUDE_DISCLOSED
    )

    # Flags for outputting entity relation data.

    SZ_ENTITY_INCLUDE_POSSIBLY_SAME_RELATIONS = 1 << 6
    SZ_ENTITY_INCLUDE_POSSIBLY_RELATED_RELATIONS = 1 << 7
    SZ_ENTITY_INCLUDE_NAME_ONLY_RELATIONS = 1 << 8
    SZ_ENTITY_INCLUDE_DISCLOSED_RELATIONS = 1 << 9
    SZ_ENTITY_INCLUDE_ALL_RELATIONS = (
        SZ_ENTITY_INCLUDE_POSSIBLY_SAME_RELATIONS
        | SZ_ENTITY_INCLUDE_POSSIBLY_RELATED_RELATIONS
        | SZ_ENTITY_INCLUDE_NAME_ONLY_RELATIONS
        | SZ_ENTITY_INCLUDE_DISCLOSED_RELATIONS
    )

    # Flags for outputting entity feature data.

    SZ_ENTITY_INCLUDE_ALL_FEATURES = 1 << 10
    SZ_ENTITY_INCLUDE_REPRESENTATIVE_FEATURES = 1 << 11

    # Flags for getting extra information about an entity.

    SZ_ENTITY_INCLUDE_ENTITY_NAME = 1 << 12
    SZ_ENTITY_INCLUDE_RECORD_SUMMARY = 1 << 13
    SZ_ENTITY_INCLUDE_RECORD_TYPES = 1 << 28
    SZ_ENTITY_INCLUDE_RECORD_DATA = 1 << 14
    SZ_ENTITY_INCLUDE_RECORD_MATCHING_INFO = 1 << 15
    SZ_ENTITY_INCLUDE_RECORD_JSON_DATA = 1 << 16
    SZ_ENTITY_INCLUDE_RECORD_UNMAPPED_DATA = 1 << 31
    SZ_ENTITY_INCLUDE_RECORD_FEATURES = 1 << 18
    SZ_ENTITY_INCLUDE_RELATED_ENTITY_NAME = 1 << 19
    SZ_ENTITY_INCLUDE_RELATED_MATCHING_INFO = 1 << 20
    SZ_ENTITY_INCLUDE_RELATED_RECORD_SUMMARY = 1 << 21
    SZ_ENTITY_INCLUDE_RELATED_RECORD_TYPES = 1 << 29
    SZ_ENTITY_INCLUDE_RELATED_RECORD_DATA = 1 << 22
    SZ_ENTITY_INCLUDE_RECORD_FEATURE_DETAILS = 1 << 35
    SZ_ENTITY_INCLUDE_RECORD_FEATURE_STATS = 1 << 36

    # Flags for extra feature data.

    SZ_ENTITY_INCLUDE_INTERNAL_FEATURES = 1 << 23
    SZ_ENTITY_INCLUDE_FEATURE_STATS = 1 << 24

    # Flags for extra matching data.

    SZ_INCLUDE_MATCH_KEY_DETAILS = 1 << 34

    # Flags for finding entity path & network data.

    SZ_FIND_PATH_STRICT_AVOID = 1 << 25
    SZ_FIND_PATH_INCLUDE_MATCHING_INFO = 1 << 30
    SZ_FIND_NETWORK_INCLUDE_MATCHING_INFO = 1 << 33

    # Flags for including search result information.

    SZ_INCLUDE_FEATURE_SCORES = 1 << 26
    SZ_SEARCH_INCLUDE_STATS = 1 << 27

    # Flag for returning with info responses.
    SZ_WITH_INFO = 1 << 62

    # Flags for exporting entity data.

    SZ_SEARCH_INCLUDE_RESOLVED = SZ_EXPORT_INCLUDE_MULTI_RECORD_ENTITIES
    SZ_SEARCH_INCLUDE_POSSIBLY_SAME = SZ_EXPORT_INCLUDE_POSSIBLY_SAME
    SZ_SEARCH_INCLUDE_POSSIBLY_RELATED = SZ_EXPORT_INCLUDE_POSSIBLY_RELATED
    SZ_SEARCH_INCLUDE_NAME_ONLY = SZ_EXPORT_INCLUDE_NAME_ONLY
    SZ_SEARCH_INCLUDE_ALL_ENTITIES = (
        SZ_SEARCH_INCLUDE_RESOLVED
        | SZ_SEARCH_INCLUDE_POSSIBLY_SAME
        | SZ_SEARCH_INCLUDE_POSSIBLY_RELATED
        | SZ_SEARCH_INCLUDE_NAME_ONLY
    )

    # Recommended settings.

    SZ_RECORD_DEFAULT_FLAGS = SZ_ENTITY_INCLUDE_RECORD_JSON_DATA

    SZ_ENTITY_DEFAULT_FLAGS = (
        SZ_ENTITY_INCLUDE_ALL_RELATIONS
        | SZ_ENTITY_INCLUDE_REPRESENTATIVE_FEATURES
        | SZ_ENTITY_INCLUDE_ENTITY_NAME
        | SZ_ENTITY_INCLUDE_RECORD_SUMMARY
        | SZ_ENTITY_INCLUDE_RECORD_DATA
        | SZ_ENTITY_INCLUDE_RECORD_MATCHING_INFO
        | SZ_ENTITY_INCLUDE_RELATED_ENTITY_NAME
        | SZ_ENTITY_INCLUDE_RELATED_RECORD_SUMMARY
        | SZ_ENTITY_INCLUDE_RELATED_MATCHING_INFO
    )

    SZ_ENTITY_BRIEF_DEFAULT_FLAGS = (
        SZ_ENTITY_INCLUDE_RECORD_MATCHING_INFO
        | SZ_ENTITY_INCLUDE_ALL_RELATIONS
        | SZ_ENTITY_INCLUDE_RELATED_MATCHING_INFO
    )

    SZ_EXPORT_DEFAULT_FLAGS = SZ_EXPORT_INCLUDE_ALL_ENTITIES | SZ_ENTITY_DEFAULT_FLAGS

    SZ_FIND_PATH_DEFAULT_FLAGS = (
        SZ_FIND_PATH_INCLUDE_MATCHING_INFO
        | SZ_ENTITY_INCLUDE_ENTITY_NAME
        | SZ_ENTITY_INCLUDE_RECORD_SUMMARY
    )

    SZ_FIND_NETWORK_DEFAULT_FLAGS = (
        SZ_FIND_NETWORK_INCLUDE_MATCHING_INFO
        | SZ_ENTITY_INCLUDE_ENTITY_NAME
        | SZ_ENTITY_INCLUDE_RECORD_SUMMARY
    )

    SZ_WHY_ENTITIES_DEFAULT_FLAGS = (
        SZ_ENTITY_DEFAULT_FLAGS
        | SZ_ENTITY_INCLUDE_INTERNAL_FEATURES
        | SZ_ENTITY_INCLUDE_FEATURE_STATS
        | SZ_INCLUDE_FEATURE_SCORES
    )

    SZ_WHY_RECORDS_DEFAULT_FLAGS = (
        SZ_ENTITY_DEFAULT_FLAGS
        | SZ_ENTITY_INCLUDE_INTERNAL_FEATURES
        | SZ_ENTITY_INCLUDE_FEATURE_STATS
        | SZ_INCLUDE_FEATURE_SCORES
    )

    SZ_WHY_RECORD_IN_ENTITY_DEFAULT_FLAGS = (
        SZ_ENTITY_DEFAULT_FLAGS
        | SZ_ENTITY_INCLUDE_INTERNAL_FEATURES
        | SZ_ENTITY_INCLUDE_FEATURE_STATS
        | SZ_INCLUDE_FEATURE_SCORES
    )

    SZ_HOW_ENTITY_DEFAULT_FLAGS = SZ_INCLUDE_FEATURE_SCORES

    SZ_VIRTUAL_ENTITY_DEFAULT_FLAGS = SZ_ENTITY_DEFAULT_FLAGS

    SZ_SEARCH_BY_ATTRIBUTES_ALL = (
        SZ_SEARCH_INCLUDE_ALL_ENTITIES
        | SZ_ENTITY_INCLUDE_REPRESENTATIVE_FEATURES
        | SZ_ENTITY_INCLUDE_ENTITY_NAME
        | SZ_ENTITY_INCLUDE_RECORD_SUMMARY
        | SZ_INCLUDE_FEATURE_SCORES
    )

    SZ_SEARCH_BY_ATTRIBUTES_STRONG = (
        SZ_SEARCH_INCLUDE_RESOLVED
        | SZ_SEARCH_INCLUDE_POSSIBLY_SAME
        | SZ_ENTITY_INCLUDE_REPRESENTATIVE_FEATURES
        | SZ_ENTITY_INCLUDE_ENTITY_NAME
        | SZ_ENTITY_INCLUDE_RECORD_SUMMARY
        | SZ_INCLUDE_FEATURE_SCORES
    )

    SZ_SEARCH_BY_ATTRIBUTES_MINIMAL_ALL = SZ_SEARCH_INCLUDE_ALL_ENTITIES

    SZ_SEARCH_BY_ATTRIBUTES_MINIMAL_STRONG = (
        SZ_SEARCH_INCLUDE_RESOLVED | SZ_SEARCH_INCLUDE_POSSIBLY_SAME
    )

    SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS = SZ_SEARCH_BY_ATTRIBUTES_ALL
