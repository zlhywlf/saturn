"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import time
from collections.abc import AsyncGenerator, Iterable
from typing import Any, Self, override

from scrapy import Request, signals
from scrapy.crawler import Crawler
from scrapy.exceptions import DontCloseSpider
from scrapy.http.response import Response
from scrapy.spiders import Spider
from scrapy.utils.misc import load_object
from scrapy.utils.request import request_from_dict

from saturn.configs import scrapy_config
from saturn.core.decisions.nodes.ListPageDecisionNode import ListPageDecisionNode
from saturn.core.decisions.nodes.PagingDecisionNode import PagingDecisionNode
from saturn.core.decisions.nodes.SavePageDecisionNode import SavePageDecisionNode
from saturn.core.decisions.SimpleDecisionEngine import SimpleDecisionEngine
from saturn.core.queues.QueuePersistentSync import QueuePersistentSync
from saturn.frameworks.scrapy.ScrapyResponse import ScrapyResponse
from saturn.models.dto.decisions.Context import Context
from saturn.models.dto.decisions.Meta import Meta
from saturn.models.dto.decisions.MetaChecker import MetaChecker
from saturn.models.dto.decisions.Task import Task


class ScrapySpider(Spider):
    """scrapy spider."""

    name: str = "saturn"

    def __init__(self, qp: QueuePersistentSync, key: str, *args: Any, **kwargs: Any) -> None:
        """Init."""
        super().__init__(*args, **kwargs)
        self._key = key
        self._batch_size = 32
        self._max_idle_time = 1
        self._qp = qp
        self._idle_start_time = 0
        self._node_map = {
            "PagingDecisionNode": PagingDecisionNode(),
            "ListPageDecisionNode": ListPageDecisionNode(),
            "SavePageDecisionNode": SavePageDecisionNode(),
        }

    @override
    def start_requests(self) -> Iterable[Request]:
        found = 0
        data = self._qp.select(self._key, 0, self._batch_size - 1, -self._batch_size, -1) or []
        for d in data:
            task = Task.model_validate_json(d)
            reqs = request_from_dict(task.model_dump(), spider=self)
            if reqs:
                yield reqs
                found += 1
        if found:
            self.logger.debug(f"Read {found} requests from '{self._key}'")

    @classmethod
    @override
    def from_crawler(cls, crawler: Crawler, *args: Any, **kwargs: Any) -> Self:
        qp_cls = load_object(scrapy_config.queue_persistent_cls)
        if not issubclass(qp_cls, QueuePersistentSync):
            raise RuntimeError
        spider = super().from_crawler(crawler, *args, qp=qp_cls(), key=scrapy_config.queue_key, **kwargs)
        if isinstance(spider, ScrapySpider):
            crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def spider_idle(self) -> None:
        """Spider idle."""
        if self._qp.get_length(self._key) > 0:
            self._idle_start_time = int(time.time())
        for req in self.start_requests():
            if self.crawler.engine:
                self.crawler.engine.crawl(req)
        idle_time = int(time.time()) - self._idle_start_time
        if self._max_idle_time != 0 and idle_time > self._max_idle_time:
            return
        raise DontCloseSpider

    @override
    async def parse(self, response: Response) -> AsyncGenerator[Any, None]:
        meta = Meta.model_validate(response.meta)
        engine = SimpleDecisionEngine(meta.meta or [], self._node_map)
        ctx = Context(checker=MetaChecker(meta=meta, type=meta.type), response=ScrapyResponse(response))
        async for result in engine.process(ctx):
            if isinstance(result, Task):
                yield request_from_dict(result.model_dump(), spider=self)
                continue
            yield result
