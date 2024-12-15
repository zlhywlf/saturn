"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, override

from pydantic import TypeAdapter
from scrapy import Request as OriginRequest, Spider
from scrapy.utils.request import request_from_dict

from saturn.core.data.Request import Request
from saturn.core.queues.Queue import Queue
from saturn.core.queues.QueuePersistentSync import QueuePersistentSync
from saturn.frameworks.scrapy.ScrapyRequest import ScrapyRequest


class ScrapyPriorityQueue(Queue[OriginRequest]):
    """scrapy priority queue."""

    def __init__(self, qp: QueuePersistentSync, spider: Spider, key: str) -> None:
        """Init."""
        self._type_adapter = TypeAdapter(dict[str, Any])
        self._spider = spider
        self._key = key % {"spider": spider.name}
        self._qp = qp

    @override
    def encode_request(self, request: Request[OriginRequest]) -> bytes:
        obj = request.revert().to_dict(spider=self._spider)
        return self._type_adapter.dump_json(obj)

    @override
    def decode_request(self, encoded_request: bytes) -> Request[OriginRequest]:
        obj = self._type_adapter.validate_json(encoded_request)
        return ScrapyRequest(request_from_dict(obj, spider=self._spider))

    @override
    def __len__(self) -> int:
        return self._qp.get_length(self._key)

    @override
    def push(self, request: Request[OriginRequest]) -> None:
        data = self.encode_request(request)
        self._qp.save(self._key, data, request.revert().priority)

    @override
    def pop(self) -> Request[OriginRequest] | None:
        results = self._qp.select(self._key)
        return self.decode_request(results) if results else None
