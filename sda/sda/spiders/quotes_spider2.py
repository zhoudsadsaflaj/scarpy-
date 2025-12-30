
from pathlib import Path
from typing import Any

import scrapy
from scrapy import cmdline
from scrapy.http import Response


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    """正常的基础操作是下面注释的部分"""
    """ async def start(self):
            urls=[
                "https://quotes.toscrape.com/page/1/",
                "https://quotes.toscrape.com/page/2/",
            ]
            for url in urls:
                yield scrapy.Request(url=url,callback=self.parse)"""
    """这里效果和上面一致，这里虽然没有明着调用parse函数，实际上是默认回调的"""
    start_urls =[
            "https://quotes.toscrape.com/page/1/",
        ]
    def parse(self, response:Response):
        for quote in response.css("div.quote"):
            yield {
                'text':quote.css("span.text::text").get(),
                'author':quote.css("small.author").get(),
                'tags':quote.css("div.tags a.tag::text").getall()
            }

            next_page=response.css("li.next a::attr(href)").get()

            if next_page is not None:
                """next_page=response.urljoin(next_page)
                yield scrapy.Request(url=next_page,callback=self.parse)"""
                yield response.follow(next_page,callback=self.parse)




if __name__=="__main__":
    #cmdline.execute("scrapy crawl quotes".split())
    cmdline.execute("scrapy crawl quotes -O quotes.json".split())
