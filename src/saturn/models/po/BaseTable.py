"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseTable(DeclarativeBase):
    """base table."""

    id: Mapped[int] = mapped_column(primary_key=True)
