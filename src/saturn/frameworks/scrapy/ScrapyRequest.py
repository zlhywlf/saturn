"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, override

from scrapy import Request as OriginRequest

from saturn.core.data.Request import Request


class ScrapyRequest(Request[OriginRequest]):
    """scrapy request."""

    def __init__(self, *, origin: OriginRequest | None = None, **kwargs: Any) -> None:
        """Init."""
        self._request = origin if origin else OriginRequest(**kwargs)

    @override
    def revert(self) -> OriginRequest:
        return self._request
