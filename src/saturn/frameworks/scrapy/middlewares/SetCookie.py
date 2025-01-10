from scrapy import Request, Spider
from scrapy.http.response import Response
from scrapy.utils.request import request_from_dict


class SetCookie:
    """set cookie."""

    async def process_request(self, request: Request, spider: Spider) -> Request | Response | None:
        """Process request."""
        if url := request.cb_kwargs.pop("set_cookie", None):
            return Request(
                url, dont_filter=True, meta=request.to_dict(spider=spider), cb_kwargs={"set_cookie_bak": True}
            )
        return None

    async def process_response(self, request: Request, response: Response, spider: Spider) -> Request | Response:
        """Process response."""
        if request.cb_kwargs.pop("set_cookie_bak", False):
            cookie_b = response.headers.get("set-cookie", None)
            if not cookie_b:
                return response
            cookie = str(cookie_b).split(";")[0]
            cookie_kv = cookie.split("=")
            return request_from_dict(request.meta | {"cookies": {cookie_kv[0]: cookie_kv[1]}}, spider=spider)
        return response
