#! /usr/bin/env python3

"""
observer_abstract.py is the abstract class for implementations of a Senzing Observer.
in the Observer pattern.

Reference:
    https://en.wikipedia.org/wiki/Observer_pattern
"""

# pylint: disable=R0903

from abc import ABC, abstractmethod

__all__ = ["ObserverAbstract"]

# -----------------------------------------------------------------------------
# ObserverAbstract
# -----------------------------------------------------------------------------


class ObserverAbstract(ABC):
    """
    ObserverAbstract is the abstract class used as a type for returning
    in process information.
    """

    # -------------------------------------------------------------------------
    # Interface definition
    # -------------------------------------------------------------------------

    @abstractmethod
    def update(self, message: str) -> None:
        """
        The `update` method of the Observer pattern.

        Args:
            message (str): A observed message.
        """
