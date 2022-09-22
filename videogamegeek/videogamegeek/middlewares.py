import logging
import json
import os
from datetime import datetime, timezone

try:
    from urllib.request import pathname2url
except ImportError:
    from urllib import pathname2url

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import Request, signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

# create logger with 'Middleware'
logger = logging.getLogger("Middleware")
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler("Middleware.log")
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


class VideogamegeekSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class VideogamegeekDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class WaybackMachineDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    cdx_url_template = (
        "https://web.archive.org/cdx/search/cdx?url={url}"
        "&output=json&fl=timestamp,original,statuscode,digest"
    )
    snapshot_url_template = "https://web.archive.org/web/{timestamp}id_/{original}"
    robots_txt = [
        "https://web.archive.org/robots.txt",
        "https://videogamegeek.com/robots.txt",
    ]
    timestamp_format = "%Y%m%d%H%M%S"

    def __init__(self, crawler):
        self.crawler = crawler
        self.logger = logging.getLogger("Middleware.WaybackMachineDownloaderMiddleware")
        self.logger.info("Creating an instance of WaybackMachineDownloaderMiddleware")

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        spider.logger.info("Started Process Request")
        spider.logger.debug(f"Request URL: {request.url}")

        if request.url in self.robots_txt:
            spider.logger.debug("Ignoring robots.txt Requests")
            return None

        if request.meta.get("override_wayback_machine"):
            spider.logger.debug("Sending Original Request")
            return None
        if request.meta.get("wayback_machine_url"):
            spider.logger.debug("Sending Wayback Machine Snapshot Request")
            return None
        if request.meta.get("wayback_machine_cdx_request"):
            spider.logger.debug("Sending Wayback Machine CDX Request")
            return None

        spider.logger.debug("Request a CDX listing of Available Snapshots")
        spider.logger.info("Finished Process Request")

        return self.build_cdx_request(request)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        spider.logger.info("Started Process Response")
        meta = request.meta
        spider.logger.debug("Request Meta: %s", meta)

        if meta.get("wayback_machine_cdx_request"):
            spider.logger.debug("Parsing CDX Requests")
            snapshot_request = self.build_snapshot_request(response, meta)

            spider.logger.debug("Schedule Snapshot Request")
            print(snapshot_request)
            self.crawler.engine.schedule(snapshot_request, spider)

        if meta.get("wayback_machine_url"):
            spider.logger.debug("Cleaning up Snapshot Responses")
            return response.replace(url=meta["wayback_machine_original_request"].url)

        spider.logger.info("Finished Process Response")
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

    def build_cdx_request(self, request):
        self.logger.info("Started Building CDX Request")

        self.logger.debug("Checking Operating System")
        if os.name == "nt":
            self.logger.debug("It is Windows Operating System")
            cdx_url = self.cdx_url_template.format(
                url=pathname2url(request.url.split("://")[1])
            )
        else:
            self.logger.debug("Not a Windows Operating System")
            cdx_url = self.cdx_url_template.format(url=pathname2url(request.url))

        cdx_request = Request(cdx_url)
        cdx_request.meta["wayback_machine_original_request"] = request
        cdx_request.meta["wayback_machine_cdx_request"] = True

        self.logger.debug("CDX Request URL: %s", cdx_request.url)
        self.logger.info("Finished Building CDX Request")
        return cdx_request

    def build_snapshot_request(self, response, meta):
        self.logger.info("Started Building Snapshot Requests")

        try:
            self.logger.debug("Parsing CDX Snapshot Data")
            data = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            self.logger.exception("Forbidden by robots.txt")
            data = []

        if not data:
            self.logger.info("No CDX Snapshot Data Available")
            self.logger.info("Continuing with Original Request")
            self.logger.info("Adding Extra Metadata to the Original Request")
            original_request = meta["wayback_machine_original_request"]
            original_request.meta.update(
                {"wayback_machine_cdx_request": False, "override_wayback_machine": True}
            )
            return original_request

        keys, rows = data[0], data[1:]
        self.logger.debug("Data Keys: %s", keys)
        self.logger.debug("Data Rows: %s", rows)

        def build_dict(row):
            self.logger.debug("Building a New Dictionary")
            new_dict = {}

            for i, key in enumerate(keys):

                if key == "timestamp":
                    self.logger.debug("A timestamp key was Found")
                    try:
                        self.logger.debug("Started formating timestamp key")
                        self.logger.debug(
                            "Timestamp Format Used: %s", self.timestamp_format
                        )
                        time = datetime.strptime(row[i], self.timestamp_format)
                        new_dict["datetime"] = time.replace(tzinfo=timezone.utc)
                        self.logger.debug("Finished formating timestamp key")
                    except ValueError:
                        self.logger.warning(
                            "Error in Wayback Date String (it happens sometimes)"
                        )
                        new_dict["datetime"] = None

                new_dict[key] = row[i]

            self.logger.debug("Finished a New Dictionary")
            return new_dict

        snapshots = list(map(build_dict, rows))
        self.logger.debug("Deleting Data Rows")
        del rows
        self.logger.debug("Deleted Data Rows")

        latest_snapshot_request = self.filter_snapshots(snapshots)
        self.logger.info("Updating URL to Point to the Snapshot")
        url = self.snapshot_url_template.format(**latest_snapshot_request)
        original_request = meta["wayback_machine_original_request"]
        snapshot_request = original_request.replace(url=url)

        # attach extension specify metadata to the request
        self.logger.info("Adding Extra Metadata to the Request")
        snapshot_request.meta.update(
            {
                "wayback_machine_original_request": original_request,
                "wayback_machine_url": snapshot_request.url,
                "wayback_machine_time": latest_snapshot_request["datetime"],
            }
        )

        self.logger.info("Finished Building Snapshot Requests")
        return snapshot_request

    def filter_snapshots(self, snapshots):
        self.logger.info("Started Filtering Snapshot Requests")
        filtered_snapshots = []

        for i, snapshot in enumerate(snapshots):
            if not snapshot["datetime"]:
                self.logger.debug("Deleting Entries with Invalid timestamps Rows")
                del snapshot[i]
                self.logger.debug("Deleted Entries with Invalid timestamps Rows")

            if snapshot["statuscode"] == "200":
                self.logger.debug("Selecting Entries with statuscode of 200")
                filtered_snapshots.append(snapshot)
                self.logger.debug("Selected Entries with statuscode of 200")

        self.logger.debug("Find Latest Snapshot with Max datetime")
        latest_datetime = max(filtered_snapshots, key=lambda x: x["datetime"])

        self.logger.info("Finished Filtering Snapshot Requests")
        return latest_datetime
