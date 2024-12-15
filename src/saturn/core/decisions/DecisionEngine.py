"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from saturn.core.data.Request import Request
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.Result import Result


class DecisionEngine[T](ABC):
    """decision engine."""

    @abstractmethod
    async def process(self, ctx: Context) -> AsyncGenerator[Result | Request[T], None]:
        """Process."""
        yield Result(id=0, name="", type=None, content=None)
