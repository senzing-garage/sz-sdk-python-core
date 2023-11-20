"""
The `observer_example` package...

"""

import queue
from typing import Any

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
    A simple Observer that can be used to receive "with-info" messages.
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        self.queue = queue.SimpleQueue()

    # -------------------------------------------------------------------------
    # ObserverExample methods for Observer pattern
    # -------------------------------------------------------------------------

    def update(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.queue.put(message)

    # -------------------------------------------------------------------------
    # Custom methods for retrieving observed methods
    #  - Models the python 'queue' method signatures.
    # -------------------------------------------------------------------------

    def empty(self) -> bool:
        return self.queue.empty()

    def get(self) -> str:
        return self.queue.get()

    def qsize(self) -> int:
        return self.queue.qsize()
