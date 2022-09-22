import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["videogamegeek.com"]
    start_urls = ["https://videogamegeek.com/browse/videogame"]

    def parse(self, response):
        next_page = response.xpath('//a[@title = "next page"]/@href').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse, dont_filter=True)
