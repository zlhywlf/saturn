"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator, Mapping
from typing import override

from saturn.core.data.Request import Request
from saturn.core.decisions.DecisionEngine import DecisionEngine
from saturn.core.decisions.DecisionNode import DecisionNode
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.Meta import Meta
from saturn.models.dto.decisions.MetaChecker import MetaChecker
from saturn.models.dto.decisions.Result import Result


class SimpleDecisionEngine(DecisionEngine):
    """simple decision engine."""

    def __init__(self, meta: list[Meta], node_map: Mapping[str, DecisionNode]) -> None:
        """Init."""
        self._meta = meta
        self._node_map = node_map

    @override
    async def process[T](self, ctx: Context) -> AsyncGenerator[Result | Request[T], None]:
        while True:
            curr_meta = ctx.checker.meta
            if curr_meta.name not in self._node_map:
                break
            node = self._node_map[curr_meta.name]
            async for result in node.handle(ctx):  # type:Result| Request[T]
                yield result
            self._decide(ctx.checker)
            next_meta = ctx.checker.meta
            if next_meta is curr_meta:
                break

    def _decide(self, checker: MetaChecker) -> None:
        for meta in self._meta:
            if meta.type == checker.type:
                checker.meta = meta
                return
