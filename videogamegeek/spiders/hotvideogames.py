import scrapy

from videogamegeek.items import HotVideoGame
from videogamegeek.itemloaders import HotVideoGameLoader


class HotVideoGameSpider(scrapy.Spider):
    name = "hotvideogames"
    allowed_domains = ["videogamegeek.com"]
    start_urls = ["https://www.videogamegeek.com/xmlapi2/hot?type=videogame"]

    def parse(self, response):
        """
        @url https://www.videogamegeek.com/xmlapi2/hot?type=videogame
        @returns items 50 50
        @returns requests 0 0
        @scrapes id rank name
        """

        self.logger.debug(f"Parse function called on {response.url}")
        for hot_items in response.xpath("/items/item"):
            item_loader = HotVideoGameLoader(HotVideoGame(), hot_items)
            item_loader.add_xpath("id", "@id")
            item_loader.add_xpath("name", "name/@value")
            item_loader.add_xpath("rank", "@rank")
            item_loader.add_xpath("image_urls", "thumbnail/@value")
            yield item_loader.load_item()
