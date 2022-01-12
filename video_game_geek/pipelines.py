# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
from datetime import timezone
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

# Getting the current date and time
dt = datetime.datetime.now(timezone.utc)
utc_time = dt.replace(tzinfo=timezone.utc)
utc_timestamp = utc_time.timestamp()

class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        spider.logger.debug(f'Duplicates pipeline called on {item!r}')
        adapter = ItemAdapter(item)
        if adapter['id'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['id'])
            return item

class TimestampPipeline:

    def process_item(self, item, spider):
        spider.logger.debug(f'Timestamp pipeline called on {item!r}')
        adapter = ItemAdapter(item)
        adapter["scraped_at"] = utc_timestamp
        return item