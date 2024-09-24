# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from day04_pachong import scrapy


class ScrapyDangdangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 通俗的说就是你要下载的数据是什么
    # 下载的路径
    src= scrapy.Field()
    # 名字
    name= scrapy.Field()
    # 价格
    price= scrapy.Field()

    pass
