"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import os

from scrapy.cmdline import execute
from scrapy.utils.project import ENVVAR, get_project_settings

import saturn.frameworks.scrapy.ScrapySpider


def main() -> None:
    """Main."""
    os.environ.setdefault(ENVVAR, __name__)
    settings = get_project_settings()
    settings.setdict(
        {
            "SPIDER_MODULES": saturn.frameworks.scrapy.ScrapySpider.__name__,
            "ITEM_PIPELINES": {"saturn.frameworks.scrapy.pipelines.SaveResultLocal.SaveResultLocal": 1},
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        },
        priority="project",
    )
    execute(["scrapy", "crawl", "saturn"], settings)


if __name__ == "__main__":
    main()
