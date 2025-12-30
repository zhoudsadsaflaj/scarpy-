import scrapy
from scrapy import cmdline
import json

class QuotesSpider(scrapy.Spider):
    name="quote"
    allowed_domains=["quotes.toscrape.com"]
    page=1
    start_urls=["https://quotes.toscrape.com/api/quotes?page=1"]

    def parse(self,response):
        data=json.load(response.text)
        for quote in data["quotes"]:
            yield {"quote":quote["text"]}
        if data["has_next"]:
            self.page+=1
            url=f"https://quotes.toscrape.com/api/quotes?page={self.page}"
            yield scrapy.Request(url=url,callback=self.parse)

if __name__=="__main__":
    cmdline.execute("scrapy crawl quotes".split())