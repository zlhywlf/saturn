"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator
from typing import override

from parsel.selector import Selector
from pydantic import BaseModel
from w3lib.html import replace_entities as w3lib_replace_entities

from saturn.core.decisions.DecisionNode import DecisionNode
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.Result import Result
from saturn.models.dto.decisions.Task import Task


class ListPageDecisionNode(DecisionNode):
    """list page decision node."""

    class Config(BaseModel):
        """config."""

        next_path: str
        recursion: bool = False
        query: str = ""
        patterns: list[str] | None = None

    @override
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        headers = await ctx.response.headers
        content_type = headers.get("Content-Type", "unknown")
        if b"html" in content_type:
            async for result in self._handle_html(ctx):
                yield result
        if b"application/json" in content_type:
            async for result in self._handle_json(ctx):
                yield result

    async def _handle_html(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        meta = ctx.checker.meta
        if not meta.config:
            return
        config = ListPageDecisionNode.Config.model_validate_json(meta.config)
        selectors = await ctx.response.extract_by_xpath(config.next_path)
        next_meta = meta if config.recursion else meta.meta
        for selector in selectors:
            url = await self._handle_a_javascript(config, selector)
            if url and next_meta:
                yield Task(
                    id=0,
                    url=await ctx.response.urljoin(url),
                    meta=next_meta,
                )

    async def _handle_a_javascript(self, config: Config, selector: Selector) -> str | None:
        if not config.patterns:
            return None
        s = []
        for path in config.patterns:
            s.extend([w3lib_replace_entities(s) for s in selector.re(path, replace_entities=False)])
        return config.query.format(*s)

    async def _handle_json(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        meta = ctx.checker.meta
        if not meta.config:
            return
        config = ListPageDecisionNode.Config.model_validate_json(meta.config)
        selectors = await ctx.response.extract_by_jmespath(config.next_path)
        next_meta = meta if config.recursion else meta.meta
        for selector in selectors:
            if config.patterns:
                s = []
                for path in config.patterns:
                    s.extend(selector.re(path))
                url = config.query.format(*s)
            else:
                url = selector.get()
            yield Task(
                id=0,
                url=await ctx.response.urljoin(url),
                meta=next_meta,
            )
