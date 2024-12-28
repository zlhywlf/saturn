import hashlib
import logging
import time
from typing import Self, override

from pydantic import TypeAdapter
from scrapy import Request, Spider
from scrapy.crawler import Crawler
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.misc import load_object
from scrapy.utils.python import to_unicode
from twisted.internet.defer import Deferred
from w3lib.url import canonicalize_url

from saturn.configs import scrapy_config
from saturn.core.rfp.RfpPersistentSync import RfpPersistentSync


class ScrapyRfpDupeFilter(BaseDupeFilter):
    """scrapy request fingerprint dupe filter."""

    logger = logging.getLogger(__name__)

    def __init__(self, *, rp: RfpPersistentSync, key: str, debug: bool = False) -> None:
        """Init."""
        self._rp = rp
        self._debug = debug
        self._key = key
        self._type_adapter = TypeAdapter(dict[str, str])

    @classmethod
    @override
    def from_crawler(cls, crawler: Crawler) -> Self:
        debug = crawler.settings.getbool("DUPEFILTER_DEBUG")
        rfp_cls = load_object(scrapy_config.rfp_persistent_cls)
        if not issubclass(rfp_cls, RfpPersistentSync):
            raise RuntimeError
        key = scrapy_config.dupe_filter_key % {"timestamp": int(time.time())}
        cls.logger.info(f"dupe filter key: {key}")
        return cls(rp=rfp_cls(), key=key, debug=debug)

    @override
    def request_seen(self, request: Request) -> bool:
        fp = self.request_fingerprint(request)
        return self._rp.exist(self._key, fp)

    def request_fingerprint(self, request: Request) -> str:
        """Request fingerprint."""
        fingerprint_data = {
            "method": to_unicode(request.method),
            "url": canonicalize_url(request.url),
            "body": (request.body or b"").hex(),
        }
        fingerprint_json = self._type_adapter.dump_json(fingerprint_data)
        return hashlib.sha1(fingerprint_json).hexdigest()  # noqa: S324

    @override
    def close(self, reason: str) -> Deferred[None] | None:
        self.clear()
        return None

    def clear(self) -> None:
        """Clear fingerprint data."""
        self._rp.delete(self._key)

    @override
    def log(self, request: Request, spider: Spider) -> None:
        if self._debug:
            self.logger.debug(f"Filtered duplicate request: {request}", extra={"spider": spider})
