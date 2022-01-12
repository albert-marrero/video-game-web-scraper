import scrapy


from scrapy.loader import ItemLoader
from ..items import HotItem


class HotItemsSpider(scrapy.Spider):
    name = 'vgg-hotitems'
    allowed_domains = ['videogamegeek.com']
    start_urls = ['https://www.videogamegeek.com/xmlapi2/hot?type=videogame']

    def parse(self, response):
        """
        @url https://www.videogamegeek.com/xmlapi2/hot?type=boardgame
        @returns items 50 50
        @returns requests 0 0
        @scrapes id rank name
        """

        self.logger.info(f'Parse function called on {response.url}')
        for hot_items in response.xpath("/items/item"):
            loader = ItemLoader(item=HotItem(), selector=hot_items)
            loader.add_xpath('id', '@id')
            loader.add_xpath('rank', '@rank')
            loader.add_xpath('name', 'name/@value')
            yield loader.load_item()