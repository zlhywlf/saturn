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

    def __init__(self, meta: Meta, node_map: Mapping[str, DecisionNode]) -> None:
        """Init."""
        self._meta = meta
        self._node_map = node_map

    @override
    async def process(self, ctx: Context) -> AsyncGenerator[Result | Request, None]:
        while True:
            curr_meta = ctx.checker.meta
            self._decide(ctx.checker)
            meta = ctx.checker.meta
            if meta is curr_meta or meta.name not in self._node_map:
                break
            node = self._node_map[meta.name]
            async for result in node.handle(ctx):
                yield result

    def _decide(self, checker: MetaChecker) -> None:
        if not self._meta.meta:
            return
        for meta in self._meta.meta:
            if meta.type == checker.type:
                checker.meta = meta
                return
