import scrapy
from itertools import islice
from scrapy.loader import ItemLoader
from scrapy.utils.misc import arg_to_iter
from urllib.parse import urlunsplit, urlencode
from video_game_geek.items import GameItem

def chucks(iterable, size=1):
    l = len(iterable)
    for item in range(0, l, size):
        yield iterable[item : min(item + size, l)]

def get_id_value(items, separator=":"):
    for item in arg_to_iter(items):
        id = item.xpath("@id").get()
        value = item.xpath("@value").get()
        yield f"{value}{separator}{id}" if id else value

def is_int(value):
    try:
        return int(value)
    except:
        return value

def is_float(value):
    try:
        return float(value)
    except:
        return value

class GamesSpider(scrapy.Spider):
    name = 'vgg-games'
    allowed_domains = ['videogamegeek.com']
    start_urls = ['https://videogamegeek.com/browse/videogame']

    def build_api_url(self, path, **kwargs):
        scheme = "https"
        netloc = "videogamegeek.com"
        query_string = urlencode(dict(kwargs))
        return urlunsplit((scheme, netloc, path, query_string, ""))

    def build_game_requests(self, ids):
        for game_id in batch(ids, 10):
            game_ids = ",".join(map(str, game_id))
            self.logger.debug(f'List of Game IDs batched: {game_ids}')
            url = self.build_api_url(
                path="xmlapi2/thing",
                stats=1,
                versions=1,
                id=game_ids,
            )
            self.logger.info(f'API URL Created: {url}')
            request = scrapy.Request(url, callback=self.parse_game)
            yield request

    def __init__(self, category=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game_ids_seen = set()
        self.game_chucks = list()
        self.api_urls = list()

    def game_batches(self):
        self.logger.debug('Start Batch Games Function')
        # convert set to list
        data = list(self.game_ids_seen)
        print(data)
        for item in chucks(data, 10):
            self.game_chucks.append(item)
        self.logger.info(f'Total Game IDs Chucks: {len(self.game_chucks)}')

    def build_game_api_urls(self):
        self.logger.debug('Start Building Game API URLs Function')
        for chuck in self.game_chucks:
            games = ",".join(map(str, chuck))
            url = self.build_api_url(
                path="xmlapi2/thing",
                stats=1,
                versions=1,
                id=games,
            )
            self.api_urls.append(url)
            self.logger.debug(f'API URL Created: {url}')
        self.logger.info(f'Total API URLs: {len(self.api_urls)}')

    def parse(self, response):
        """
        @url https://videogamegeek.com/browse/boardgame/
        @returns items 0 0
        @returns requests 0 11
        """

        self.logger.debug(f'Parse Function Called on {response.url}')
        # get all game ids from page
        game_ids_extracted = response.xpath(
            './/td[contains(@class, "collection_object")]//a/@href'
        ).re(r"^/\w+/(\d+).*$")
        self.logger.info(f'Total Game IDs Extracted: {len(game_ids_extracted)}')
        # print(response.status)

        self.game_ids_seen.update(game_ids_extracted)
        self.logger.info(f'Total Game IDs Seen: {len(self.game_ids_seen)}')
        
        # yield from self.build_game_requests(game_ids)

        # not last page, figure out next page
        next_page = response.xpath('//a[@title = "next page"]/@href').get()
        next_page = None
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
        # last page
        if next_page is None:
            self.game_batches()
            self.build_game_api_urls()
            for url in self.api_urls:
                request = scrapy.Request(url, callback=self.parse_game)
                yield request

    def parse_game(self, response):
        """
        @url https://www.videogamegeek.com/xmlapi2/thing?id=141874&stats=1
        @returns items 1 1
        @returns requests 0 100
        @scrapes type id name alternate_names description \
            platform genre theme franchise series mode \
            min_players max_players release_date developer \
            publisher compilation number_of_votes average \
            bayes_average standard_deviation median complexity \
            rankings
        """
        self.logger.info(f'Parse Game function called on {response.url}')
        for game in response.xpath("/items/item"):
            loader = ItemLoader(item=GameItem(), selector=game)
            loader.add_xpath('type', '@type')
            loader.add_xpath('id', '@id')
            loader.add_xpath('name', 'name[@type = "primary"]/@value')
            loader.add_xpath('alternate_names', 'name[@type = "alternate"]/@value')
            loader.add_xpath('description', 'description')
            loader.add_value(
                'platform',
                get_id_value(
                    game.xpath('link[@type = "videogameplatform"]')
                )
            )
            loader.add_value(
                'genre',
                get_id_value(
                    game.xpath('link[@type = "videogamegenre"]')
                )
            )
            loader.add_value(
                'theme',
                get_id_value(
                    game.xpath('link[@type = "videogametheme"]')
                )
            )
            loader.add_value(
                'franchise',
                get_id_value(
                    game.xpath('link[@type = "videogamefranchise"]')
                )
            )
            loader.add_value(
                'series',
                get_id_value(
                    game.xpath('link[@type = "videogameseries"]')
                )
            )
            loader.add_value(
                'mode',
                get_id_value(
                    game.xpath('link[@type = "videogamemode"]')
                )
            )
            loader.add_xpath("min_players", "minplayers/@value")
            loader.add_xpath("max_players", "maxplayers/@value")
            loader.add_xpath("release_date", "releasedate/@value")
            loader.add_value(
                'developer',
                get_id_value(
                    game.xpath('link[@type = "videogamedeveloper"]')
                )
            )
            loader.add_value(
                'publisher',
                get_id_value(
                    game.xpath('link[@type = "videogamepublisher"]')
                )
            )
            loader.add_value(
                'compilation',
                get_id_value(
                    game.xpath('link[@type = "videogamecompilation"]')
                )
            )
            loader.add_xpath('number_of_votes', 'statistics/ratings/usersrated/@value')
            loader.add_xpath('average', 'statistics/ratings/average/@value')
            loader.add_xpath('bayes_average', 'statistics/ratings/bayesaverage/@value')
            loader.add_xpath('standard_deviation', 'statistics/ratings/stddev/@value')
            loader.add_xpath('median', 'statistics/ratings/median/@value')
            loader.add_xpath('complexity', 'statistics/ratings/averageweight/@value')

            for rank in game.xpath('statistics/ratings/ranks/rank'):
                rankings = {
                    'id': is_int(rank.xpath('@id').get()),
                    'name': rank.xpath('@name').get(),
                    'friendly_name': rank.xpath('@friendlyname').get(),
                    'rank': is_int(rank.xpath('@value').get()),
                    'bayes_average': is_float(rank.xpath('@bayesaverage').get())
                }
                loader.add_value('rankings', rankings)

            for item in game.xpath('versions/item[@type = "videogameversion"]'):
                versions = {
                    'release_date': item.xpath('releasedate/@value').get(),
                    'platform': item.xpath('link[@type = "videogameplatform"]/@value').get(),
                    'publisher': item.xpath('link[@type = "videogamepublisher"]/@value').get(),
                    'developer': item.xpath('link[@type = "videogamedeveloper"]/@value').get(),
                    'media': item.xpath('link[@type = "videogamemedia"]/@value').get(),
                }
                loader.add_value('versions', versions)

            yield loader.load_item()
