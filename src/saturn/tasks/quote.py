from saturn import ListPageDecisionNode, SavePageDecisionNode, Task

enter = Task(
    name="quote",
    url="https://quotes.toscrape.com/",
    dont_filter=True,
)

paging = Task(
    name=ListPageDecisionNode.__name__,
    config=ListPageDecisionNode.Config(
        next_path="//ul//a",
        recursion=True,
        query="{0}",
        patterns=[r'href="([^"]+)"'],
    ).model_dump_json(),
)

item = Task(
    name=ListPageDecisionNode.__name__,
    config=ListPageDecisionNode.Config(
        next_path="//div[@class='quote']//a",
        query="{0}",
        patterns=[r'href="([^"]+)"'],
    ).model_dump_json(),
)

save = Task(name=SavePageDecisionNode.__name__)

enter >> paging >> [item >> save]
