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


class ListPageDecisionNode(DecisionNode):
    """list page decision node."""

    @override
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        meta = ctx.checker.meta
        config = ListPageDecisionNode.Config.model_validate_json(meta.config)
        ctx.checker.type = 1 if config.needed else 2
        paths = await ctx.response.extract_by_xpath(config.paths)
        names = await ctx.response.extract_by_xpath(config.names)
        if meta.sub and paths and names:
            for path, _ in zip(paths, names, strict=False):
                yield Task(
                    id=0,
                    url=await ctx.response.urljoin(path),
                    meta=meta.sub,
                    headers={},
                    cookies={},
                    flags=[],
                    cb_kwargs={},
                    cls="scrapy.http.request.Request",
                )

    class Config(NodeConfig):
        """config."""

        paths: str
        names: str
