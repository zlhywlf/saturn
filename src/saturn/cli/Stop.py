"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel, Field

from saturn.configs.AppEnum import AppEnum


class Stop(BaseModel):
    """stop."""

    app: AppEnum = Field(..., description="the name of app")
