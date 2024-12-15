"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import time
from collections.abc import Iterable
from typing import Any, Self, override

from scrapy import FormRequest, Request, signals
from scrapy.crawler import Crawler
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import Spider
from scrapy.utils.misc import load_object

from saturn.configs.ScrapyConfig import ScrapyConfig
from saturn.core.queues.QueuePersistentSync import QueuePersistentSync
from saturn.models.dto.decisions.Task import Task


class ScrapySpider(Spider):
    """scrapy spider."""

    def __init__(self, qp: QueuePersistentSync, key: str, *args: Any, **kwargs: Any) -> None:
        """Init."""
        super().__init__(*args, **kwargs)
        self._key = key
        self._batch_size = 32
        self._max_idle_time = 0
        self._qp = qp
        self._idle_start_time = 0

    @override
    def start_requests(self) -> Iterable[Request]:
        found = 0
        data = self._qp.select(self._key, 0, self._batch_size - 1, -self._batch_size, -1) or []
        for d in data:
            task = Task.model_validate_json(d)
            url = task.url
            method = task.method.upper()
            meta = task.meta.model_dump()
            reqs = FormRequest(url=url, method=method, meta={"decision": meta})
            if reqs:
                yield reqs
                found += 1
        if found:
            self.logger.debug(f"Read {found} requests from '{self._key}'")

    @classmethod
    @override
    def from_crawler(cls, crawler: Crawler, *args: Any, **kwargs: Any) -> Self:
        config = ScrapyConfig()
        qp_cls = load_object(config.queue_persistent_cls)
        if not issubclass(qp_cls, QueuePersistentSync):
            raise RuntimeError
        spider = super().from_crawler(crawler, *args, qp=qp_cls(), key=config.queue_key, **kwargs)
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
