from pathlib import Path
from typing import Any

import scrapy
from scrapy import cmdline
from scrapy.http import Response


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    async def start(self):
        urls=[
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response:Response):
        page=response.url.split("/")[-2]
        filename=f'quotes-{page}.html'
        Path(filename).write_bytes(response.body)
        self.log(f"save file{filename}")

if __name__=="__main__":
    cmdline.execute("scrapy crawl quotes".split())
