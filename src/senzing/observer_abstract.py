#! /usr/bin/env python3

"""
observer_abstract.py is the abstract class for all implementations of a Senzing
'with_info' observer.
"""

from abc import ABC, abstractmethod
from typing import Any

__all__ = ["ObserverAbstract"]

# -----------------------------------------------------------------------------
# G2ConfigAbstract
# -----------------------------------------------------------------------------


class ObserverAbstract(ABC):
    """
    ObserverAbstract is...
    """

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def update(self, message: str, *args: Any, **kwargs: Any) -> None:
        """
        The `update` method of the Observer pattern.

        Args:
            message (str): A observed message
        """
