"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel

from saturn.models.dto.decisions.Task import Task


class MetaChecker(BaseModel, arbitrary_types_allowed=True):
    """meta checker."""

    meta: Task
    type: int
