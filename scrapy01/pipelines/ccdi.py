# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from scrapy01.pipelines.base import MongoPipeline


class CcDiPipeline(MongoPipeline):

    collection_name = 'ccdi'