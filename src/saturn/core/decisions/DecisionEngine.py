from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.Result import Result
from saturn.models.dto.decisions.Task import Task


class DecisionEngine(ABC):
    """decision engine."""

    @abstractmethod
    async def process(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        """Process."""
        yield Result(name="", type=None, content=None)
