from pathlib import Path

import execjs
from scrapy import Request, Spider
from scrapy.http.response import Response
from scrapy.utils.request import request_from_dict


class RSVMPCookie:
    """rs vmp cookie."""

    def __init__(self) -> None:
        """Init."""
        parent = Path(__file__).absolute().parent
        with (
            (parent / "rs_vmp.js").open(encoding="utf-8") as f,
            (parent / "rs_vmp_core.js").open(encoding="utf-8") as c,
        ):
            self._code = f.read().replace("$_core", c.read())

    async def process_request(self, request: Request, spider: Spider) -> Request | Response | None:
        """Process request."""
        cb_kwargs = request.cb_kwargs
        if url := cb_kwargs.pop("rs_vmp", None):
            return Request(url, dont_filter=True, meta=request.to_dict(spider=spider))
        return None

    async def process_response(self, request: Request, response: Response, spider: Spider) -> Request | Response:
        """Process response."""
        if response.status != 412:
            return response
        content = response.xpath("//head/meta[@r='m']/@content").get()
        head = response.xpath("//head/script[not(@src)]/text()").get()
        if not content or not head:
            return response
        code = self._code.replace("$_content", content).replace("$_head", head)
        cookie = str(execjs.compile(code).call("get_cookie")).split(";")[0]
        cookie_kv = cookie.split("=")
        return request_from_dict(request.meta | {"cookies": {cookie_kv[0]: cookie_kv[1]}}, spider=spider)
