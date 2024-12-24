"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import math
from collections.abc import AsyncGenerator
from typing import override

from pydantic import BaseModel, TypeAdapter

from saturn.core.decisions.DecisionNode import DecisionNode
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.Result import Result
from saturn.models.dto.decisions.Task import Task


class PagingDecisionNode(DecisionNode):
    """paging decision node."""

    class Config(BaseModel):
        """config."""

        total: str
        size: str
        query: str = ""
        headers: str | None = None

    def __init__(self) -> None:
        """Init."""
        self._headers_adapter = TypeAdapter(dict[bytes, list[bytes]])

    @override
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        headers = await ctx.response.headers
        content_type = headers.get("Content-Type", "unknown")
        if b"application/json" in content_type:
            async for result in self._handle_json(ctx):
                yield result

    async def _handle_json(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        meta = ctx.checker.meta
        if not meta.config:
            return
        config = PagingDecisionNode.Config.model_validate_json(meta.config)
        total = (await ctx.response.extract_by_jmespath(config.total)).get()
        size = (await ctx.response.extract_by_jmespath(config.size)).get()
        if total is None or size is None:
            return
        pages = math.ceil(int(total) / int(size))
        headers = None
        if config.headers:
            headers = self._headers_adapter.validate_json(config.headers)
        for page in range(pages):
            if page > 1:
                break
            query = config.query.format(page + 1, size)
            yield Task(
                id=0, url=await ctx.response.url, method="POST", meta=meta.meta, body=query.encode(), headers=headers
            )
