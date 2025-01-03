from typing import Any

from saturn.core.decisions.nodes.ListPageDecisionNode import ListPageDecisionNode
from saturn.core.decisions.nodes.PagingDecisionNode import PagingDecisionNode
from saturn.core.decisions.nodes.SavePageDecisionNode import SavePageDecisionNode
from saturn.models.dto.decisions.Task import Task

__all__ = ["ListPageDecisionNode", "PagingDecisionNode", "SavePageDecisionNode", "Task"]


def entry_task(
    *,
    name: str,
    url: str,
    cookies: dict[str, str] | None = None,
    headers: dict[bytes, list[bytes]] | None = None,
    method: str = "GET",
    body: bytes = b"",
    encoding: str = "utf-8",
    priority: int = 0,
    dont_filter: bool = False,
    flags: list[str] | None = None,
    cb_kwargs: dict[str, Any] | None = None,
    callback: str | None = None,
    errback: str | None = None,
) -> Task:
    """Entry task."""
    return Task(
        url=url,
        cookies=cookies,
        headers=headers,
        method=method,
        body=body,
        encoding=encoding,
        priority=priority,
        dont_filter=dont_filter,
        flags=flags,
        cb_kwargs=cb_kwargs,
        callback=callback,
        errback=errback,
        name=name,
    )


def list_task(
    *,
    url: str | None = None,
    cookies: dict[str, str] | None = None,
    headers: dict[bytes, list[bytes]] | None = None,
    method: str = "GET",
    body: bytes = b"",
    encoding: str = "utf-8",
    priority: int = 0,
    dont_filter: bool = False,
    flags: list[str] | None = None,
    cb_kwargs: dict[str, Any] | None = None,
    callback: str | None = None,
    errback: str | None = None,
    next_path: str,
    recursion: bool = False,
    query: str = "",
    patterns: list[str] | None = None,
    url_patterns: list[str] | None = None,
    url_encrypt: str | None = None,
    convert_json: bool = False,
) -> Task:
    """List task."""
    return Task(
        url=url,
        cookies=cookies,
        headers=headers,
        method=method,
        body=body,
        encoding=encoding,
        priority=priority,
        dont_filter=dont_filter,
        flags=flags,
        cb_kwargs=cb_kwargs,
        callback=callback,
        errback=errback,
        name=ListPageDecisionNode.__name__,
        config=ListPageDecisionNode.Config(
            next_path=next_path,
            recursion=recursion,
            query=query,
            patterns=patterns,
            url_patterns=url_patterns,
            url_encrypt=url_encrypt,
            convert_json=convert_json,
        ).model_dump_json(),
    )


def paging_task(
    *,
    url: str | None = None,
    cookies: dict[str, str] | None = None,
    headers: dict[bytes, list[bytes]] | None = None,
    method: str = "GET",
    body: bytes = b"",
    encoding: str = "utf-8",
    priority: int = 0,
    dont_filter: bool = False,
    flags: list[str] | None = None,
    cb_kwargs: dict[str, Any] | None = None,
    callback: str | None = None,
    errback: str | None = None,
    total: str = "",
    size: str = "",
    query: str = "",
    pages: str = "",
    is_url_paging: bool = False,
    total_pattern: str = "",
    size_pattern: str = "",
) -> Task:
    """Paging task."""
    return Task(
        url=url,
        cookies=cookies,
        headers=headers,
        method=method,
        body=body,
        encoding=encoding,
        priority=priority,
        dont_filter=dont_filter,
        flags=flags,
        cb_kwargs=cb_kwargs,
        callback=callback,
        errback=errback,
        name=PagingDecisionNode.__name__,
        config=PagingDecisionNode.Config(
            total=total,
            size=size,
            query=query,
            pages=pages,
            is_url_paging=is_url_paging,
            total_pattern=total_pattern,
            size_pattern=size_pattern,
        ).model_dump_json(),
    )


save_item = Task(name=SavePageDecisionNode.__name__)
