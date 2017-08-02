# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose


class MovItem(ItemLoader):
    default_output_processor = TakeFirst()


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    thumb = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    duration = scrapy.Field()
    post_date = scrapy.Field()
    video_url = scrapy.Field()
    views_num = scrapy.Field()
    channel = scrapy .Field()

