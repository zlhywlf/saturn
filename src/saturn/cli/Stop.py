from pydantic import BaseModel, Field

from saturn.configs.AppEnum import AppEnum


class Stop(BaseModel):
    """stop."""

    app: AppEnum = Field(..., description="the name of app")
