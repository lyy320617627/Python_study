# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from day04_pachong import scrapy


class ScarpyMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    src= scrapy.Field()
    name= scrapy.Field()
