"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Optional

from pydantic import BaseModel


class Meta(BaseModel):
    """meta."""

    id: int
    name: str
    type: int
    config: str
    meta: list["Meta"] | None = None
    sub: Optional["Meta"] = None
    file_name: str | None = None
