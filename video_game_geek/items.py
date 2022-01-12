# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

class GameItem(scrapy.Item):
    # define the fields for your item here like:
    type = scrapy.Field(
        serializer=str,
        output_processor=TakeFirst(),
    )
    id = scrapy.Field(
        serializer=int,
        output_processor=TakeFirst(),
    )
    thumbnail = scrapy.Field()
    image = scrapy.Field()
    name = scrapy.Field(
        serializer=str,
        output_processor=TakeFirst(),
    )
    alternate_names = scrapy.Field()
    description = scrapy.Field(
        serializer=str,
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    platform = scrapy.Field()
    genre = scrapy.Field()
    theme = scrapy.Field()
    franchise = scrapy.Field()
    series = scrapy.Field()
    mode = scrapy.Field()
    min_players = scrapy.Field(
        serializer=int,
        output_processor=TakeFirst(),
    )
    max_players = scrapy.Field(
        serializer=int,
        output_processor=TakeFirst(),
    )
    release_date = scrapy.Field(
        serializer=str,
        output_processor=TakeFirst(),
    )
    developer = scrapy.Field()
    publisher = scrapy.Field()
    compilation = scrapy.Field()
    number_of_votes = scrapy.Field(
        serializer=int,
        output_processor=TakeFirst(),
    )
    average = scrapy.Field(
        serializer=float,
        output_processor=TakeFirst(),
    )
    bayes_average = scrapy.Field(
        serializer=float,
        output_processor=TakeFirst(),
    )
    standard_deviation = scrapy.Field(
        serializer=float,
        output_processor=TakeFirst(),
    )
    median = scrapy.Field(
        serializer=float,
        output_processor=TakeFirst(),
    )
    complexity = scrapy.Field(
        serializer=float,
        output_processor=TakeFirst(),
    )
    rankings = scrapy.Field()
    scraped_at = scrapy.Field(
        serializer=float
    )

class HotItem(scrapy.Item):
    # define the fields for your item here like:
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
    scraped_at = scrapy.Field(
        serializer=float
    )
