"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import asyncio
from pathlib import Path

import scrapy

from saturn.models.dto.decisions.Result import Result
import time


class SaveResultLocal:
    """save result local."""

    async def process_item(self, item: Result, spider: scrapy.Spider) -> Result:
        """Do."""
        Path("./dist").mkdir(exist_ok=True)
        spider.log(f"{item.type!s},{len(item.content or '')}")
        loop = asyncio.get_event_loop()
        file_name = item.name if item.name else f"{len(item.content or '')}"
        if item.content:
            with open(f"./dist/{file_name}-{int(time.time())}.{'html' if 'html' in str(item.type) else 'unknown'}", "wb") as f:  # noqa: ASYNC230 PTH123
                await loop.run_in_executor(None, f.write, item.content)
        return item
