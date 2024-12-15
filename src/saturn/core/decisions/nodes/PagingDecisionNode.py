"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import math
import re
from collections.abc import AsyncGenerator
from typing import override

from saturn.core.data.Request import Request
from saturn.core.decisions.DecisionNode import DecisionNode
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.NodeConfig import NodeConfig
from saturn.models.dto.decisions.Result import Result


class PagingDecisionNode[T](DecisionNode[T]):
    """paging decision node."""

    @override
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Request[T], None]:
        meta = ctx.checker.meta
        config = PagingDecisionNode.Config.model_validate_json(meta.config)
        ctx.checker.type = 1 if config.needed else 2
        text = await ctx.response.text
        limit_match = re.search(config.limit, text)
        limit = limit_match.group(1) if limit_match else None
        count_match = re.search(config.count, text)
        count = count_match.group(1) if count_match else None
        url_match = re.search(config.url, text)
        url = url_match.group(1) if url_match else None
        pages = math.ceil(int(count) / int(limit))  # type:ignore  [arg-type]
        if meta.sub:
            for page in range(pages):
                if page > 1:
                    break
                yield self.request_factory.create(
                    url=url,
                    formdata={"pageNumber": f"{page + 1}", "pageSize": limit},
                    meta={"decision": meta.sub},
                )

    class Config(NodeConfig):
        """config."""

        limit: str
        count: str
        url: str
