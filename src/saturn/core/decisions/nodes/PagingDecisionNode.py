"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import math
import re
from collections.abc import AsyncGenerator
from typing import override

from pydantic import TypeAdapter

from saturn.core.decisions.DecisionNode import DecisionNode
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.NodeConfig import NodeConfig
from saturn.models.dto.decisions.Result import Result
from saturn.models.dto.decisions.Task import Task


class PagingDecisionNode(DecisionNode):
    """paging decision node."""

    def __init__(self) -> None:
        """Init."""
        self._type_adapter = TypeAdapter(dict[str, str])

    @override
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        meta = ctx.checker.meta
        config = PagingDecisionNode.Config.model_validate_json(meta.config)
        ctx.checker.type = 1 if config.needed else 2
        text = await ctx.response.text
        limit_match = re.search(config.limit, text)
        limit = limit_match.group(1) if limit_match else None
        count_match = re.search(config.count, text)
        count = count_match.group(1) if count_match else None
        url_match = re.search(config.url, text)
        url = url_match.group(1) if url_match.group() else None
        pages = math.ceil(int(count) / int(limit))  # type:ignore  [arg-type]
        if meta.sub:
            for page in range(pages):
                if page > 1:
                    break
                yield Task(
                    id=0,
                    url=url if url else (await ctx.response.urljoin("")),
                    method=config.method,
                    body=(config.body % {"page": page + 1, "limit": limit}).encode(),
                    meta=meta.sub,
                    headers={b"Content-Type": [b"application/x-www-form-urlencoded"]},
                    cookies={},
                    flags=[],
                    cb_kwargs={},
                    cls="scrapy.http.request.form.FormRequest",
                )

    class Config(NodeConfig):
        """config."""

        limit: str
        count: str
        url: str
        body: str
        method: str
