from pydantic import Field
from pydantic_settings import BaseSettings


class ScrapyConfig(BaseSettings, env_prefix="SATURN_SCRAPY_", env_file=".env", env_file_encoding="utf-8"):
    """scrapy config."""

    dupe_filter_key: str = Field(default="dupe_filter:%(timestamp)s")
    queue_key: str = Field(default="saturn:requests")
    rfp_persistent_cls: str = Field(default="saturn.web.rfp.RFPPersistentSync.RFPPersistentSync")
    queue_persistent_cls: str = Field(default="saturn.web.queues.RedisQueuePersistentSync.RedisQueuePersistentSync")
