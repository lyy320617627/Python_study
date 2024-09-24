from day04_pachong import scrapy
from day04_pachong.scrapy import LinkExtractor
from day04_pachong.scrapy import CrawlSpider, Rule

from read_book_101.read_book_101.items import ReadBook101Item


class ReadSpider(CrawlSpider):
    name = "read"
    allowed_domains = ["www.dushu.com"]
    start_urls = ["https://www.dushu.com/book/1188.html"]

    rules = (Rule(LinkExtractor(allow=r"/book/1188_\d+\.html"),
                                callback="parse_item",
                                follow=False),)

    def parse_item(self, response):
        img_list=response.xpath("//div[@class='bookslist']//img")
        for img in img_list:
            name=img.xpath("./@alt").extract_first()
            src=img.xpath("./@data-original").extract_first()
            book=ReadBook101Item(name=name,src=src)
            yield book
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
