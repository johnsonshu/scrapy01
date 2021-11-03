import datetime
import socket
import scrapy

from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor

from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.http import Request
from shutil import which

from scrapy01.items import CommonItem

from shutil import which
class Zc2techSpider(CrawlSpider):
    SELENIUM_DRIVER_NAME = 'firefox'
    SELENIUM_DRIVER_EXECUTABLE_PATH = which('geckodriver')
    SELENIUM_DRIVER_ARGUMENTS=['-headless']  # '--headles

    def house_keeping_item(self,item,response):
        # Housekeeping fields
        item['meta_url'] = response.url
        item['meta_project'] = self.settings.get('BOT_NAME')
        item['meta_spider'] = self.name
        item['meta_server'] = socket.gethostname()
        item['meta_date'] = datetime.datetime.now()

