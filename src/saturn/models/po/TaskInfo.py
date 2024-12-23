"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any

from pydantic import TypeAdapter
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from saturn.models.dto.decisions.Task import Task
from saturn.models.po.BaseTable import BaseTable


class TaskInfo(BaseTable):
    """task info."""

    __tablename__ = "task"

    pid: Mapped[int | None] = mapped_column(ForeignKey("task.id"), nullable=True)
    mid: Mapped[int | None] = mapped_column(ForeignKey("task.id"), nullable=True)
    name: Mapped[str] = mapped_column(String())
    url: Mapped[str | None] = mapped_column(String(), nullable=True)
    method: Mapped[str] = mapped_column(String(), default="GET")
    type: Mapped[int] = mapped_column(Integer(), default=0)
    cls: Mapped[str | None] = mapped_column(String(), nullable=True)
    config: Mapped[str | None] = mapped_column(String(), nullable=True)
    cookies: Mapped[str | None] = mapped_column(String(), nullable=True)
    headers: Mapped[str | None] = mapped_column(String(), nullable=True)
    body: Mapped[str | None] = mapped_column(String(), nullable=True)
    encoding: Mapped[str | None] = mapped_column(String(), nullable=True)
    priority: Mapped[int] = mapped_column(Integer(), default=0)
    dont_filter: Mapped[bool] = mapped_column(Boolean(), default=False)
    flags: Mapped[str | None] = mapped_column(String(), nullable=True)
    cb_kwargs: Mapped[str | None] = mapped_column(String(), nullable=True)
    callback: Mapped[str | None] = mapped_column(String(), nullable=True)
    errback: Mapped[str | None] = mapped_column(String(), nullable=True)
    sub: Mapped[list["TaskInfo"]] = relationship(
        lazy="immediate",
        primaryjoin=lambda: (TaskInfo.pid == TaskInfo.id),
    )
    meta: Mapped["TaskInfo"] = relationship(
        lazy="immediate",
        primaryjoin=lambda: (TaskInfo.mid == TaskInfo.id),
        remote_side=[mid],
        uselist=False,
    )

    @classmethod
    def load_task(cls, info: "TaskInfo") -> Task:
        """Load task."""
        cookies_adapter = TypeAdapter(dict[str, str])
        headers_adapter = TypeAdapter(dict[bytes, list[bytes]])
        flags_adapter = TypeAdapter(list[str])
        cb_kwargs_adapter = TypeAdapter(dict[str, Any])
        return Task(
            id=info.id,
            name=info.name,
            url=info.url,
            cls=info.cls if info.cls else "scrapy.http.request.Request",
            config=info.config,
            type=info.type,
            cookies=cookies_adapter.validate_json(info.cookies) if info.cookies else None,
            headers=headers_adapter.validate_json(info.headers) if info.headers else None,
            method=info.method,
            body=info.body.encode() if info.body else b"",
            encoding=info.encoding or "utf-8",
            priority=info.priority,
            dont_filter=info.dont_filter,
            flags=flags_adapter.validate_json(info.flags) if info.flags else None,
            cb_kwargs=cb_kwargs_adapter.validate_json(info.cb_kwargs) if info.cb_kwargs else None,
            sub=[cls.load_task(_) for _ in info.sub] if info.sub else None,
            meta=cls.load_task(info.meta) if info.meta else None,
            callback=info.callback,
            errback=info.errback,
        )
