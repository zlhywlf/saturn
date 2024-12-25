"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import asyncio
import time
from pathlib import Path

import scrapy

from saturn.models.dto.decisions.Result import Result


class SaveResultLocal:
    """save result local."""

    async def process_item(self, item: Result, spider: scrapy.Spider) -> Result:
        """Do."""
        Path("./dist").mkdir(exist_ok=True)
        spider.log(f"{item.type!s},{len(item.content or '')}")
        loop = asyncio.get_event_loop()
        file_name = (
            item.name.replace("/", "_")
            .replace(":", "_")
            .replace("?", "_")
            .replace("\n", "")
            .replace(" ", "")
            .replace("\r","")
            .replace("\t","")
            if item.name
            else f"{len(item.content or '')}"
        )
        file_name = file_name[:120]
        if item.content:
            with open(  # noqa: ASYNC230 PTH123
                f"./dist/{file_name}-{time.time()}.{'html' if 'html' in str(item.type) else 'json'}", "wb"
            ) as f:
                await loop.run_in_executor(None, f.write, item.content)
        return item
