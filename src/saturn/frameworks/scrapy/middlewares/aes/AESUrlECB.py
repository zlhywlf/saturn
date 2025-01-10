import re

from scrapy import Request, Spider
from scrapy.http.response import Response

from saturn.utils.EncryptUtil import encrypt_aes_ecb


class AESUrlECB:
    """url aes ecb."""

    async def process_request(self, request: Request, spider: Spider) -> Request | Response | None:  # noqa ARG002
        """Process request."""
        key = request.cb_kwargs.pop("url_aes_ecb", None)
        rep = request.cb_kwargs.pop("url_aes_ecb_rep", None)
        if key and rep:
            url = request.url
            m = re.search(rep, url)
            if not m:
                return None
            origin = m.group(1)
            s = encrypt_aes_ecb(origin, key).replace("/", "^")[:-2]
            return request.replace(url=url.replace(origin, s))
        return None
