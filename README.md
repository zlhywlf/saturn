# saturn

## 初始化项目

```shell
pip3 install -e .[dev] -i https://mirrors.aliyun.com/pypi/simple;
pre-commit install --install-hooks;
```

## debug spider

```python
from scrapy.cmdline import execute

execute(["scrapy", "crawl", "spider's name"])
```
