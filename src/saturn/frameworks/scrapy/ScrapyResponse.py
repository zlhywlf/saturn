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
        content_type = origin.headers.get("Content-Type")
        self._response = origin
        self._is_json = bool(content_type and b"application/json" in content_type)

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

    @property
    @override
    async def url(self) -> str:
        return self._response.url

    @override
    async def extract(self, query: str) -> SelectorList[Selector]:
        return self._response.jmespath(query) if self._is_json else self._response.xpath(query)

    @property
    @override
    def is_json(self) -> bool:
        return self._is_json
