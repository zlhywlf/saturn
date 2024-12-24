"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator, Mapping
from typing import override

from saturn.core.decisions.DecisionEngine import DecisionEngine
from saturn.core.decisions.DecisionNode import DecisionNode
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.Result import Result
from saturn.models.dto.decisions.Task import Task


class SimpleDecisionEngine(DecisionEngine):
    """simple decision engine."""

    def __init__(self, meta: list[Task], node_map: Mapping[str, DecisionNode]) -> None:
        """Init."""
        self._meta = meta
        self._node_map = node_map

    @override
    async def process(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        while True:
            curr_meta = ctx.checker.meta
            if curr_meta.name not in self._node_map:
                break
            node = self._node_map[curr_meta.name]
            async for result in node.handle(ctx):
                yield result
            if not self._meta:
                break
            next_meta = ctx.checker.meta = self._meta.pop()
            if not next_meta:
                break
