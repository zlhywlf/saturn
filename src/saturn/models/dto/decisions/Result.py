from pydantic import BaseModel


class Result(BaseModel):
    """result."""

    type: str | bytes | None
    content: bytes | None
    name: str
