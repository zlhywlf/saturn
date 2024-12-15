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
    settings.setdict({"SPIDER_MODULES": saturn.frameworks.scrapy.ScrapySpider.__name__}, priority="project")
    execute(["scrapy", "crawl", "saturn"], settings)


if __name__ == "__main__":
    main()
