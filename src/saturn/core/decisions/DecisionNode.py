from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.Result import Result
from saturn.models.dto.decisions.Task import Task


class DecisionNode(ABC):
    """decision node."""

    @abstractmethod
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        """Handle."""
        yield Result(name="", type=None, content=None)
