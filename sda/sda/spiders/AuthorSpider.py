from typing import Any

import scrapy
from scrapy import cmdline
from scrapy.http import Response


class AuthorSpider(scrapy.Spider):
    name = "author"

    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        author_links=response.css(".author + a")
        yield from response.follow_all(author_links,callback=self.parse_author)

        page_links=response.css("li.next a")

        yield from response.follow_all(page_links,callback=self.parse)


    def parse_author(self,response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        yield {
            'author':extract_with_css('h3.author-title::text'),
            'birthdate':extract_with_css('span.author-born-data::text'),
            'biograph':extract_with_css('div.author-description::text')
        }

if __name__=="__main__":
    cmdline.execute("scrapy crawl author".split())