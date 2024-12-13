"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from typing import Any


class QueueClient(ABC):
    """queue client."""

    @abstractmethod
    def sadd(self, name: str, value: str | float) -> int:
        """Sadd."""

    @abstractmethod
    def delete(self, name: str) -> None:
        """Delete."""

    @abstractmethod
    def zcard(self, name: str) -> int:
        """Zcard."""

    @abstractmethod
    def execute_command(self, *args: Any, **options: Any) -> None:
        """Execute command."""

    @abstractmethod
    def pop_priority(self, key: str, start: int = 0, end: int = 0, min_: int = 0, max_: int = 0) -> list[Any]:
        """Pop priority."""
