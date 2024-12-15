"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod


class Request[T](ABC):
    """request."""

    @abstractmethod
    def revert(self) -> T:
        """Revert."""

    def __call__(self) -> T:
        """Revert."""
        return self.revert()
