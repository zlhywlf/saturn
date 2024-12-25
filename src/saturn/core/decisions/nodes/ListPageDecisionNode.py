"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator, Callable
from typing import ClassVar, override

from parsel.selector import Selector
from pydantic import BaseModel
from w3lib.html import replace_entities as w3lib_replace_entities

from saturn.core.decisions.DecisionNode import DecisionNode
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.Result import Result
from saturn.models.dto.decisions.Task import Task
from saturn.utils.EncryptUtil import modify_url


class ListPageDecisionNode(DecisionNode):
    """list page decision node."""

    ENCRYPT_FUNC: ClassVar[dict[str, Callable[[str], str]]] = {"modify_url": modify_url}

    class Config(BaseModel):
        """config."""

        next_path: str
        recursion: bool = False
        query: str = ""
        patterns: list[str] | None = None
        url_patterns: list[str] | None = None
        url_encrypt: str | None = None

    @override
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        meta = ctx.checker.meta
        if not meta.config:
            return
        config = ListPageDecisionNode.Config.model_validate_json(meta.config)
        selectors = await ctx.response.extract(config.next_path)
        next_meta = meta if config.recursion else meta.meta
        for selector in selectors:
            query = await self._handle_a_javascript(config, selector)
            if query is not None and next_meta:
                full_url = (
                    meta.url
                    if meta.url
                    else (
                        (await ctx.response.url)
                        if meta.method.lower() == "post"
                        else (await ctx.response.urljoin(query))
                    )
                )
                full_url = await self._handle_url(full_url, config, selector)
                full_url = await self._handle_encrypt_url(full_url, config)
                body = query.encode() if meta.method.lower() == "post" else b""
                yield Task(
                    id=0,
                    url=full_url,
                    meta=next_meta,
                    method=meta.method,
                    headers=meta.headers,
                    body=body,
                )

    async def _handle_a_javascript(self, config: Config, selector: Selector) -> str | None:
        if not config.patterns:
            return config.query
        s = []
        for path in config.patterns:
            s.extend([w3lib_replace_entities(s) for s in selector.re(path, replace_entities=False) if s])
        if config.query and not s:
            return None
        return config.query.format(*s)

    async def _handle_url(self, url: str, config: Config, selector: Selector) -> str:
        if not config.url_patterns:
            return url
        s = []
        for path in config.url_patterns:
            s.extend([w3lib_replace_entities(s) for s in selector.re(path, replace_entities=False) if s])
        if not s:
            return url
        return url.format(*s)

    async def _handle_encrypt_url(self, url: str, config: Config) -> str:
        if not config.url_encrypt or config.url_encrypt not in self.ENCRYPT_FUNC:
            return url
        return self.ENCRYPT_FUNC[config.url_encrypt](url)
