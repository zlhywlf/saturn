"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from scrapy import Request as OriginRequest

from saturn.core.data.Request import Request


class ScrapyRequest(Request[OriginRequest]):
    """scrapy request."""

    def __init__(self, request: OriginRequest) -> None:
        """Init."""
        self._request = request

    @override
    def revert(self) -> OriginRequest:
        return self._request
