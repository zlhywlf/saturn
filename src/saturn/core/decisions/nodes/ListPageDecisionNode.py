"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import re
from collections.abc import AsyncGenerator
from typing import override

from parsel.selector import Selector
from pydantic import BaseModel

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
        page_path: str = "/"

    def __init__(self) -> None:
        """Init."""
        self._pattern = re.compile(r"\b\d+\b")
        self._full_url_pattern = re.compile(r'https?://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:/[^"\s]*)?')

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
        selectors = await ctx.response.extract_by_xpath(config.next_path)
        next_meta = meta if config.recursion else meta.sub
        for selector in selectors:
            url = None
            if selector.root.tag == "a":
                url = await self._handle_a(config, selector)
            if selector.root.tag == "div":
                url = await self._handle_div(selector)
            if url and next_meta:
                yield Task(
                    id=0,
                    url=await ctx.response.urljoin(url),
                    meta=next_meta,
                    headers={},
                    cookies={},
                    flags=[],
                    cb_kwargs={},
                    cls="scrapy.http.request.Request",
                )

    async def _handle_a(self, config: Config, selector: Selector) -> str | None:
        if href := selector.attrib.get("href"):
            return await self._handle_a_javascript(config, selector) if href.startswith(("javascript:", "#")) else href
        return await self._handle_a_javascript(config, selector)

    async def _handle_a_javascript(self, config: Config, selector: Selector) -> str | None:
        match = self._pattern.search(selector.xpath(config.page_path).extract_first() or "")
        if not match:
            return None
        return config.query % {"page": match.group()}

    async def _handle_div(self, selector: Selector) -> str | None:
        if match := self._full_url_pattern.search(selector.attrib.get("onclick") or ""):
            return match.group()
        return None
