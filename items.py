# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SnbookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    auth_name = scrapy.Field()
    content_img = scrapy.Field()
    content = scrapy.Field()
    raw_price = scrapy.Field()
    discout_price = scrapy.Field()
