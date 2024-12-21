"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator
from typing import override

from parsel.selector import Selector

from saturn.core.decisions.DecisionNode import DecisionNode
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.NodeConfig import NodeConfig
from saturn.models.dto.decisions.Result import Result
from saturn.models.dto.decisions.Task import Task


class ListPageDecisionNode(DecisionNode):
    """list page decision node."""

    @override
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        headers = await ctx.response.headers
        content_type = headers.get("Content-Type", "unknown")
        if b"html" in content_type:
            async for result in self._handle_html(ctx):
                yield result

    async def _handle_html(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        meta = ctx.checker.meta
        config = ListPageDecisionNode.Config.model_validate_json(meta.config)
        ctx.checker.type = 1 if config.needed else 2
        selectors = await ctx.response.extract_by_xpath(config.next_path)
        for selector in selectors:
            url = None
            if selector.root.tag == "a":
                url = await self._handle_a(selector)
            if url:
                yield Task(
                    id=0,
                    url=await ctx.response.urljoin(url),
                    meta=meta if config.recursion else meta.sub,
                    headers={},
                    cookies={},
                    flags=[],
                    cb_kwargs={},
                    cls="scrapy.http.request.Request",
                )
            break

    async def _handle_a(self, selector: Selector) -> str | None:
        if href := selector.attrib.get("href"):
            return href
        return None

    class Config(NodeConfig):
        """config."""

        next_path: str
        recursion: bool = False
