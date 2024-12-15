"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Self

from pydantic import BaseModel


class Result(BaseModel):
    """result."""

    type: str | bytes | None
    content: bytes | None
    name: str

    def __call__(self) -> Self:
        """Self."""
        return self
