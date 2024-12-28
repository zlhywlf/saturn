from pydantic import BaseModel

from saturn.models.dto.decisions.Task import Task


class MetaChecker(BaseModel, arbitrary_types_allowed=True):
    """meta checker."""

    meta: Task
    type: int
