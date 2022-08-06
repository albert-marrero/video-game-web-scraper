# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


class VideoGameGeekItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HotVideoGame(scrapy.Item):
    id = scrapy.Field(
        serializer=int,
        output_processor=TakeFirst(),
    )
    rank = scrapy.Field(
        serializer=int,
        output_processor=TakeFirst(),
    )
    name = scrapy.Field(
        serializer=str,
        output_processor=TakeFirst(),
    )
    scraped_at = scrapy.Field(serializer=str)
    image_urls = scrapy.Field()
    images = scrapy.Field()
