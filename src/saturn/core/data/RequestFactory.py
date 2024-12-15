"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from typing import Any

from saturn.core.data.Request import Request


class RequestFactory[T](ABC):
    """request factory."""

    @abstractmethod
    def create(self, **kwargs: Any) -> Request[T]:
        """Create."""
