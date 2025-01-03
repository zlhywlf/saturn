from typing import Any, Optional, Union

from pydantic import BaseModel


class Task(BaseModel):
    """task."""

    id: int = 0
    name: str = "unknown"
    url: str | None = None
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

    def __rshift__(self, n: Union["Task", list["Task"]]) -> "Task":
        """>>."""
        t = self
        while t.meta:
            t = t.meta
        if isinstance(n, list):
            t.sub = [self._check(_) for _ in n]
        else:
            t.meta = self._check(n)
        return self

    def _check(self, n: "Task") -> "Task":
        if n is self:
            msg = "Recursive error"
            raise RuntimeError(msg)
        n.id = -1
        return n
