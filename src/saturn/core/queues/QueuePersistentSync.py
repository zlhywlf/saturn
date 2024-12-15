"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod


class QueuePersistentSync(ABC):
    """queue persistent."""

    @abstractmethod
    def get_length(self, key: str) -> int:
        """Get length."""

    @abstractmethod
    def save(self, key: str, data: bytes, priority: int) -> None:
        """Save."""

    @abstractmethod
    def select(self, key: str) -> bytes | None:
        """Select."""

    @abstractmethod
    def delete(self, key: str) -> bytes | None:
        """Delete."""
