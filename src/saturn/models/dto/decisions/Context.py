"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel

from saturn.core.data.Response import Response
from saturn.models.dto.decisions.MetaChecker import MetaChecker


class Context(BaseModel, arbitrary_types_allowed=True):
    """context."""

    response: Response
    checker: MetaChecker
