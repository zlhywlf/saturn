"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from saturn.models.dto.decisions.Task import Task


class Queue(ABC):
    """queue."""

    @abstractmethod
    def encode_task(self, task: Task) -> bytes:
        """Encode a task object."""

    @abstractmethod
    def decode_task(self, encoded_task: bytes) -> Task:
        """Decode a task previously encoded."""

    @abstractmethod
    def __len__(self) -> int:
        """Len."""

    @abstractmethod
    def push(self, task: Task) -> None:
        """Push."""

    @abstractmethod
    def pop(self) -> Task | None:
        """Pop."""

    @abstractmethod
    def clear(self) -> None:
        """Clear."""
