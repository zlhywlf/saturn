"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import math
import re
from collections.abc import AsyncGenerator
from typing import override

from pydantic import BaseModel

from saturn.core.decisions.DecisionNode import DecisionNode
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.Result import Result
from saturn.models.dto.decisions.Task import Task


class PagingDecisionNode(DecisionNode):
    """paging decision node."""

    class Config(BaseModel):
        """config."""

        total: str = ""
        size: str = ""
        query: str = ""
        pages: str = ""
        is_url_paging: bool = False
        total_pattern: str = ""
        size_pattern: str = ""

    @override
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        meta = ctx.checker.meta
        if not meta.config:
            return
        config = PagingDecisionNode.Config.model_validate_json(meta.config)
        if config.pages:
            d = (await ctx.response.extract(config.pages)).get()
            if d is None:
                return
            pages = int(d)
        else:
            total = (await ctx.response.extract(config.total)).get()
            size = (await ctx.response.extract(config.size)).get()
            if total is None or size is None:
                return
            if config.total_pattern:
                m = re.search(config.total_pattern, total)
                if m is None:
                    return
                total = m.group(1)
            if config.size_pattern:
                m = re.search(config.size_pattern, size)
                if m is None:
                    return
                size = m.group(1)
            pages = math.ceil(int(total) / int(size))
        url = meta.url if meta.url else (await ctx.response.url)
        for page in range(pages):
            if page > 1:
                break
            full_url = url.format(page + 1) if config.is_url_paging else url
            query = config.query.format(page + 1) if not config.is_url_paging else config.query
            body = query.encode() if meta.method.lower() == "post" else b""
            yield Task(
                id=0,
                url=full_url,
                method=meta.method,
                meta=meta.meta,
                body=body,
                headers=meta.headers,
            )
