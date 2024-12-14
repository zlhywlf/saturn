"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from scrapy import Request as OriginRequest

from saturn.core.data.Request import Request
from saturn.core.data.RequestFactory import RequestFactory
from saturn.frameworks.scrapy.ScrapyRequest import ScrapyRequest


class ScrapyRequestFactory(RequestFactory[OriginRequest]):
    """scrapy request factory."""

    @override
    def create(self, request: OriginRequest) -> Request[OriginRequest]:
        return ScrapyRequest(request)
