"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from saturn.core.data.Request import Request
from saturn.core.data.RequestFactory import RequestFactory
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.Result import Result


class DecisionNode(ABC):
    """decision node."""

    def __init__(self, request_factory: RequestFactory) -> None:
        """Init."""
        self._request_factory = request_factory

    @property
    def request_factory(self) -> RequestFactory:
        """Request factory."""
        return self._request_factory

    @abstractmethod
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Request, None]:
        """Handle."""
        yield Result(id=0, name="", type=None, content=None)
