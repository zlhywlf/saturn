"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Self, override

from scrapy import Request as OriginRequest
from scrapy.core.scheduler import BaseScheduler
from scrapy.crawler import Crawler
from scrapy.dupefilters import BaseDupeFilter
from scrapy.spiders import Spider
from scrapy.statscollectors import StatsCollector
from scrapy.utils.misc import load_object
from twisted.internet.defer import Deferred

from saturn.configs import scrapy_config
from saturn.core.queues.Queue import Queue
from saturn.core.queues.QueuePersistentSync import QueuePersistentSync
from saturn.frameworks.scrapy.ScrapyPriorityQueue import ScrapyPriorityQueue
from saturn.frameworks.scrapy.ScrapyRequest import ScrapyRequest
from saturn.frameworks.scrapy.ScrapyRfpDupeFilter import ScrapyRfpDupeFilter


class ScrapyScheduler(BaseScheduler):
    """scrapy scheduler."""

    def __init__(
        self,
        qp: QueuePersistentSync,
        dupe_filter: BaseDupeFilter,
        queue_key: str,
        idle_before_close: int = 0,
        stats: StatsCollector | None = None,
        *,
        persist: bool = False,
        flush_on_start: bool = False,
    ) -> None:
        """Init."""
        self._qp = qp
        self._persist = persist
        self._flush_on_start = flush_on_start
        self._idle_before_close = idle_before_close if idle_before_close >= 0 else 0
        self._stats = stats
        self._dupe_filter = dupe_filter
        self._spider: Spider | None = None
        self._queue: Queue[OriginRequest] | None = None
        self._queue_key = queue_key

    @classmethod
    @override
    def from_crawler(cls, crawler: Crawler) -> Self:
        settings = crawler.settings
        kwargs = {
            "persist": settings.getbool("SCHEDULER_PERSIST"),
            "flush_on_start": settings.getbool("SCHEDULER_FLUSH_ON_START"),
            "idle_before_close": settings.getint("SCHEDULER_IDLE_BEFORE_CLOSE"),
            "stats": crawler.stats,
            "dupe_filter": ScrapyRfpDupeFilter.from_crawler(crawler),
            "queue_key": scrapy_config.queue_key,
        }
        qp_cls = load_object(scrapy_config.queue_persistent_cls)
        if not issubclass(qp_cls, QueuePersistentSync):
            raise RuntimeError
        return cls(qp=qp_cls(), **kwargs)  # type: ignore [arg-type]

    @override
    def open(self, spider: Spider) -> Deferred[None] | None:
        self._spider = spider
        self._queue = ScrapyPriorityQueue(self._qp, spider, self._queue_key)
        if self._flush_on_start:
            self.flush()
        if len(self.queue):
            spider.log(f"Resuming crawl ({len(self.queue)} requests scheduled)")
        return None

    def flush(self) -> None:
        """Flash."""
        if isinstance(self._dupe_filter, ScrapyRfpDupeFilter):
            self._dupe_filter.clear()
        self.queue.clear()

    @override
    def close(self, reason: str) -> Deferred[None] | None:
        if not self._persist:
            self.flush()
        return None

    @override
    def enqueue_request(self, request: OriginRequest) -> bool:
        if not request.dont_filter and self._spider and self.dupe_filter.request_seen(request):
            self.dupe_filter.log(request, self._spider)
            return False
        if self._stats:
            self._stats.inc_value("scheduler/enqueued/redis", spider=self._spider)
        self.queue.push(ScrapyRequest(origin=request))
        return True

    @override
    def next_request(self) -> OriginRequest | None:
        request = self.queue.pop()
        if request and self._stats:
            self._stats.inc_value("scheduler/dequeued/redis", spider=self._spider)
        return request.revert() if request else None

    @override
    def has_pending_requests(self) -> bool:
        return len(self.queue) > 0

    @property
    def queue(self) -> Queue[OriginRequest]:
        """Queue."""
        if self._queue is None:
            msg = "The queue cannot be None"
            raise RuntimeError(msg)
        return self._queue

    @property
    def dupe_filter(self) -> BaseDupeFilter:
        """Dupe filter."""
        return self._dupe_filter

    @property
    def persist(self) -> bool:
        """Persist."""
        return self._persist
