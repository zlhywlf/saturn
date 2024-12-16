"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator
from typing import override

from saturn.core.decisions.DecisionNode import DecisionNode
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.NodeConfig import NodeConfig
from saturn.models.dto.decisions.Result import Result
from saturn.models.dto.decisions.Task import Task


class NextPageDecisionNode(DecisionNode):
    """next page decision node."""

    @override
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        meta = ctx.checker.meta
        config = NextPageDecisionNode.Config.model_validate_json(meta.config)
        ctx.checker.type = 1 if config.needed else 2
        next_paths = await ctx.response.extract_by_xpath(config.next_path)
        if next_paths:
            for path in next_paths:
                if not path.startswith("/"):
                    continue
                yield Task(
                    id=0,
                    url=await ctx.response.urljoin(path),
                    meta=meta,
                    headers={},
                    cookies={},
                    flags=[],
                    cb_kwargs={},
                    cls="scrapy.http.request.Request",
                )

    class Config(NodeConfig):
        """config."""

        next_path: str
