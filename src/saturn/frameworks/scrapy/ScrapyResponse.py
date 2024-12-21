"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, override

from parsel.selector import Selector, SelectorList
from scrapy.http.response import Response as OriginResponse

from saturn.core.data.Response import Response


class ScrapyResponse(Response):
    """scrapy response."""

    def __init__(self, origin: OriginResponse) -> None:
        """Init."""
        self._response = origin

    @override
    async def urljoin(self, url: str) -> str:
        return self._response.urljoin(url)

    @property
    @override
    async def text(self) -> str:
        return self._response.text

    @property
    @override
    async def headers(self) -> dict[str, bytes]:
        return self._response.headers

    @property
    @override
    async def body(self) -> bytes:
        return self._response.body

    @property
    @override
    async def meta(self) -> dict[str, Any]:
        return self._response.meta

    @override
    async def extract_by_xpath(self, query: str) -> SelectorList[Selector]:
        return self._response.xpath(query)
