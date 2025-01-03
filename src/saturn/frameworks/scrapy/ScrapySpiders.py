from scrapy.utils.misc import walk_modules

from saturn.frameworks.scrapy.ScrapySpider import ScrapySpider
from saturn.models.dto.decisions.Task import Task

g = globals()
index = 0
cls = None
for module in walk_modules("saturn.tasks"):
    for obj in vars(module).values():
        if isinstance(obj, Task) and obj.id == 0:
            cls_name = f"Spider{index}"
            cls = type(cls_name, (ScrapySpider,), {"TASK": obj, "name": obj.name})
            g.setdefault(cls_name, cls)
            index += 1
cls = None
