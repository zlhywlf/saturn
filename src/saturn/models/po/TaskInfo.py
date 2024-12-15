"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from saturn.models.dto.decisions.Task import Task
from saturn.models.po.BaseTable import BaseTable
from saturn.models.po.MetaInfo import MetaInfo


class TaskInfo(BaseTable):
    """task info."""

    __tablename__ = "task"

    url: Mapped[str] = mapped_column(String())
    method: Mapped[str] = mapped_column(String())
    meta: Mapped[MetaInfo] = relationship(lazy="immediate")

    @classmethod
    def load_task(cls, task_info: "TaskInfo") -> Task:
        """Load task."""
        return Task(
            id=task_info.id,
            url=task_info.url,
            method=task_info.method,
            meta=MetaInfo.load_meta(task_info.meta).model_dump(),
            headers={},
            cookies={},
            cb_kwargs={},
            flags=[],
            cls="",
        )
