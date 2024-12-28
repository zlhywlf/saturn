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
        selectors = await ctx.response.extract("//head/title/text()") if not ctx.response.is_json else None
        yield Result(
            type=(await ctx.response.headers).get("Content-Type", "unknown"),
            content=await ctx.response.body,
            name=f"[{url}]{selectors[0].get()}" if selectors else url,
        )
