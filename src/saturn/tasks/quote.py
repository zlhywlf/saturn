from saturn import entry_task, list_task, save_item

quote = entry_task(
    name="quote",
    url="https://quotes.toscrape.com/",
    dont_filter=True,
)

paging = list_task(next_path="//ul//a", query="{0}", patterns=[r'href="([^"]+)"'], recursion=True)

item = list_task(next_path="//div[@class='quote']//a", query="{0}", patterns=[r'href="([^"]+)"'])

quote >> paging >> [item >> save_item]
