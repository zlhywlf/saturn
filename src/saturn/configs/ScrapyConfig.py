"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class ScrapyConfig(BaseSettings, env_prefix="SATURN_SCRAPY_", env_file=".env", env_file_encoding="utf-8"):
    """scrapy config."""

    dupe_filter_key: str = Field(default="dupe_filter:%(timestamp)s")
    rfp_persistent_cls: str = Field(default="saturn.core.rfp.RFPPersistentSync.RFPPersistentSync")
