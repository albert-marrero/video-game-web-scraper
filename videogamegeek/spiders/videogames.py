import scrapy


class VideogamesSpider(scrapy.Spider):
    name = "videogames"
    allowed_domains = ["videogamegeek.com"]
    start_urls = ["http://videogamegeek.com/browse/videogame"]

    def parse(self, response):
        next_page = response.xpath('//a[@title = "next page"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
