"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator
from typing import override

from saturn.core.decisions.DecisionNode import DecisionNode
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.Result import Result
from saturn.models.dto.decisions.Task import Task


class SavePageDecisionNode(DecisionNode):
    """save page decision node."""

    @override
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Task, None]:
        url = await ctx.response.url
        selectors = await ctx.response.extract_by_xpath("//head/title/text()")
        yield Result(
            type=(await ctx.response.headers).get("Content-Type", "unknown"),
            content=await ctx.response.body,
            name=f"[{url}]{selectors[0].get()}" if selectors else url,
        )
