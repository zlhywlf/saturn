"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator
from typing import override

from saturn.core.data.Request import Request
from saturn.core.decisions.DecisionNode import DecisionNode
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.NodeConfig import NodeConfig
from saturn.models.dto.decisions.Result import Result


class ListPageDecisionNode[T](DecisionNode[T]):
    """list page decision node."""

    @override
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Request[T], None]:
        meta = ctx.checker.meta
        config = ListPageDecisionNode.Config.model_validate_json(meta.config)
        ctx.checker.type = 1 if config.needed else 2
        paths = await ctx.response.extract_by_xpath(config.paths)
        names = await ctx.response.extract_by_xpath(config.names)
        if meta.sub and paths and names:
            for path, name in zip(paths, names, strict=False):
                yield self.request_factory.create(
                    url=await ctx.response.urljoin(path),
                    meta={"decision": meta.sub, "file_name": name},
                )

    class Config(NodeConfig):
        """config."""

        paths: str
        names: str
