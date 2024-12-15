"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from saturn.core.data.Request import Request


class Queue[T](ABC):
    """queue."""

    @abstractmethod
    def encode_request(self, request: Request[T]) -> bytes:
        """Encode a request object."""

    @abstractmethod
    def decode_request(self, encoded_request: bytes) -> Request[T]:
        """Decode an request previously encoded."""

    @abstractmethod
    def __len__(self) -> int:
        """Len."""

    @abstractmethod
    def push(self, request: Request[T]) -> None:
        """Push."""

    @abstractmethod
    def pop(self) -> Request[T] | None:
        """Pop."""

    @abstractmethod
    def clear(self) -> None:
        """Clear."""
