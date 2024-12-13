"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel


class Result(BaseModel):
    """result."""

    id: int
    type: str | bytes | None
    content: bytes | None
    name: str
