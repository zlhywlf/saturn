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
    def select(self, key: str, start: int, end: int, min_: int, max_: int) -> list[bytes] | None:
        """Select."""

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete."""
