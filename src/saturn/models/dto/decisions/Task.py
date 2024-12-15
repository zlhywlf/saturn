"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any

from pydantic import BaseModel, Field


class Task(BaseModel):
    """task."""

    id: int
    url: str
    callback: str | None = None
    errback: str | None = None
    headers: dict[bytes, list[bytes]]
    method: str = "GET"
    body: bytes = b""
    cookies: dict[str, str]
    meta: dict[str, Any]
    encoding: str = "utf-8"
    priority: int = 0
    dont_filter: bool = False
    flags: list[str]
    cb_kwargs: dict[str, Any]
    cls: str = Field(..., serialization_alias="_class")
