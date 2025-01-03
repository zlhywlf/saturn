from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseTable(DeclarativeBase):
    """base table."""

    id: Mapped[int] = mapped_column(primary_key=True)
