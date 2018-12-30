# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RealEstateScrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Estate(scrapy.Item):
    location = scrapy.Field()
    price = scrapy.Field()
    floor = scrapy.Field()
    built = scrapy.Field()
    renewed = scrapy.Field()
    url = scrapy.Field()
    size = scrapy.Field()
    distance = scrapy.Field()
