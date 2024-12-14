"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from saturn.core.data.Request import Request


class RequestFactory[T](ABC):
    """request factory."""

    @abstractmethod
    def create(self, request: T) -> Request[T]:
        """Create."""
