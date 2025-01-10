from pydantic import BaseModel


class Result(BaseModel):
    """result."""

    type: str | bytes | None
    content: bytes | None
    name: str

    def __str__(self) -> str:
        """Str."""
        return f"{self.type!r}: {self.name}"
