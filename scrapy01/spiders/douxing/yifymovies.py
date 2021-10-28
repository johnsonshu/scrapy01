import datetime
import socket
import scrapy

import re
from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor


from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.http import Request

from selenium import webdriver
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from scrapy01.items import CommonItem
from scrapy01.common.zc2tech import Zc2techSpider
from scrapy01.common.conditions import *

# https://ww1.yifymovies.pro/

class YifymoviesSpider(Zc2techSpider):
    name = 'yifymoves'

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy01.pipelines.yifymovies.YifymoviesPipeline': 300,
            'scrapy01.pipelines.myimage.MyImagesPipeline': 1
            # 'scrapy.pipelines.images.ImagesPipeline': 1
        },
        'IMAGES_STORE' : 'file_image/yi/yifymovies',
        'FILES_STORE'  : 'file_image/yi/yifymovies',        
        
    }

    allowed_domains = ['ww1.yifymovies.pro']
    # start_urls = ['https://ww1.yifymovies.pro/movies-list/']

    def start_requests(self):
        urls = [
            'https://ww1.yifymovies.pro/movies-list/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # rules = (
    #     # Last Link:
    #     Rule(LinkExtractor(allow=(r'/movies\-list/page/')),follow=False),

    #     # Extract links matching 'item.php' and parse them with the spider's method parse_item
    #     #Rule(LinkExtractor(allow=(r'/movie/', )), callback='parse_item'),
    # )
        
    def parse(self, response):
        reDetail = re.compile(r"/movie/")
        pageLinks = response.xpath('//ul[@class="pagination"]/li/a/@href').getall()
        movieLinkes = response.xpath('//div[contains(@class,"movies-list")]//div[@class="ml-item"]/a/@href').getall()
        for link in pageLinks:
            yield Request(link, callback=self.parse)

        for link in movieLinkes:
            yield SeleniumRequest(url=link, callback=self.parse_item \
                    , wait_time=10 , wait_until=carousel_done())
            
                
    def parse_item(self, response):
        item = CommonItem()
        #item['id'] = response.xpath('//div[@class="flater_tab"]/div/h2/text()').re(r'ID: (\d+)')
        item['title'] = response.xpath('//div[@class="mvic-desc"]/h3/text()').get()
        item['description'] = response.xpath('//div[@itemprop="description"]/p/text()').get()
        # Genre,Director,Actors ... Maybe we can parse the html later
        item['info'] = response.xpath('//div[@class="mvic-info"]/node()').extract()


        item['cover_image_url'] = ''
        item['image_urls'] = []

        # cover image
        # style="background-image: url('https://image.tmdb.org/t/p/w185/zSqJ1qFq8NXFfi7JeIYMlzyR0dx.jpg');">               
        coverImageStyle = response.xpath('//div[@class="mvi-content"]/div[contains(@class,"mvic-thumb")]/@style').get()
        m = re.search(r"url\('([^']+)'\)", coverImageStyle)
        if m:
            item['image_urls'].append(m.group(1))
            item['cover_image_url'] = m.group(1)

        #images
        imageNodes = response.xpath('//div[@class="owl-item"]//img').getall()
        for img in imageNodes:
            imgSrc = Selector(text=img).xpath('//img/@src').get()            
            item['image_urls'].append(imgSrc)

        self.house_keeping_item(item,response)                
        return item



   