"""
The `observer_example` package shows a simple Observer that can be used
when calling G2Engine calls using Observers.
"""

import queue

from .observer_abstract import ObserverAbstract

# Metadata

__all__ = ["ObserverExample"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-11-20"
__updated__ = "2023-11-20"


# -----------------------------------------------------------------------------
# ObserverExample class
# -----------------------------------------------------------------------------


class ObserverExample(ObserverAbstract):
    """
    A simple Observer that can be used to receive processing messages.
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
    ) -> None:
        """
        Create an example Observer for use with Senzing processing processing.
        """
        self.queue: queue.SimpleQueue[str] = queue.SimpleQueue()

    # -------------------------------------------------------------------------
    # ObserverExample methods for Observer pattern
    # -------------------------------------------------------------------------

    def update(self, message: str) -> None:
        """
        The `update` method of an Observer pattern.

        Args:
            message (str): A JSON document containing processing information.
        """
        self.queue.put(message)

    # -------------------------------------------------------------------------
    # Custom methods for retrieving observed methods
    #  - Models the python 'queue' method signatures.
    # -------------------------------------------------------------------------

    def empty(self) -> bool:
        """
        Determine if there are no messages.

        Returns:
            bool: True, if no message exist.
        """
        return self.queue.empty()

    def get(self) -> str:
        """
        Get the oldest message.

        Returns:
            str: A JSON document containing process information.
        """
        return str(self.queue.get())

    def size(self) -> int:
        """
        The number of messages available.

        Returns:
            int: The number of messages that are available.
        """
        return self.queue.qsize()
