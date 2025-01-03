BOT_NAME = "saturn"
SPIDER_MODULES = ["saturn.frameworks.scrapy.ScrapySpiders"]
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
)
ROBOTSTXT_OBEY = False
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
ITEM_PIPELINES = {"saturn.frameworks.scrapy.pipelines.SaveResultLocal.SaveResultLocal": 1}
