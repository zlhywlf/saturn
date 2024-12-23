"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    """task."""

    id: int
    name: str = "unknown"
    url: str | None = None
    cls: str = Field("scrapy.http.request.Request", serialization_alias="_class")
    config: str | None = None
    type: int = 0
    cookies: dict[str, str] | None = None
    headers: dict[bytes, list[bytes]] | None = None
    method: str = "GET"
    body: bytes = b""
    encoding: str = "utf-8"
    priority: int = 0
    dont_filter: bool = False
    flags: list[str] | None = None
    cb_kwargs: dict[str, Any] | None = None
    sub: list["Task"] | None = None
    meta: Optional["Task"] = None
    callback: str | None = None
    errback: str | None = None
