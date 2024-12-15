"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from saturn.models.dto.decisions.Meta import Meta
from saturn.models.po.BaseTable import BaseTable


class MetaInfo(BaseTable):
    """meta info."""

    __tablename__ = "meta"

    pid: Mapped[int | None] = mapped_column(ForeignKey("meta.id"), nullable=True)
    sid: Mapped[int | None] = mapped_column(ForeignKey("meta.id"), nullable=True)
    tid: Mapped[int] = mapped_column(ForeignKey("task.id"), nullable=True)
    name: Mapped[str] = mapped_column(String())
    type: Mapped[int] = mapped_column(Integer(), default=0)
    config: Mapped[str | None] = mapped_column(String(), nullable=True)
    meta: Mapped[list["MetaInfo"]] = relationship(
        lazy="immediate",
        primaryjoin=lambda: (MetaInfo.pid == MetaInfo.id),
    )
    sub: Mapped["MetaInfo"] = relationship(
        lazy="immediate",
        primaryjoin=lambda: (MetaInfo.sid == MetaInfo.id),
        remote_side=[sid],
        uselist=False,
    )

    @classmethod
    def load_meta(cls, meta_info: "MetaInfo") -> Meta:
        """Load meta."""
        return Meta(
            id=meta_info.id,
            name=meta_info.name,
            type=meta_info.type,
            meta=[cls.load_meta(_) for _ in meta_info.meta] if meta_info.meta else None,
            config=meta_info.config or "",
            sub=cls.load_meta(meta_info.sub) if meta_info.sub else None,
        )
