import datetime
import socket
import scrapy

import re
from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.http import Request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scrapy01.common.selenium import SeleniumRequest

from scrapy01.items import CommonItem, YifyMoviesItem
from scrapy01.common.zc2tech import Zc2techSpider
from scrapy01.common.conditions import *

# https://ww1.yifymovies.pro/

class YifymoviesSpider(Zc2techSpider):
    name = 'yifymovies'

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
        
    def parse(self, response):
        reDetail = re.compile(r"/movie/")
        pageLinks = response.xpath('//ul[@class="pagination"]/li/a/@href').getall()
        movieLinkes = response.xpath('//div[contains(@class,"movies-list")]//div[@class="ml-item"]/a/@href').getall()
        
        # TODO: comment/uncomment to limit/add all pages, before deploying to production environment
        for link in pageLinks:
            yield Request(link, callback=self.parse)

        for link in movieLinkes:
            yield SeleniumRequest(url=link, callback=self.parse_item \
                    , wait_time=10 , wait_until=carousel_done())
            
                
    def parse_item(self, response):
        item = YifyMoviesItem()
        soup = BeautifulSoup(response.text, 'html.parser')

        #item['id'] = response.xpath('//div[@class="flater_tab"]/div/h2/text()').re(r'ID: (\d+)')
        item['title'] = response.xpath('//div[@class="mvic-desc"]/h3/text()').get()
        item['description'] = response.xpath('//div[@itemprop="description"]/p/text()').get()
        # Genre,Director,Actors ... Maybe we can parse the html later
        # item['info_html'] = response.xpath('//div[@class="mvic-info"]/node()').extract()
        item['info_html'] = soup.find("div", {"class":"mvic-info" }).prettify()

        # response.xpath not work for "list-dl" and "list-sub" DIV,
        # I have to use other parser:BeautifulSoup
        item['download_links'] = []
       
        listdl = soup.find("div", id= "list-dl")
        rows = listdl.select('a[class*="lnk-lnk"]')
        for r in rows:
            link = r['href']
            if (link == None or link.strip() == ""):
                continue
            server = r.find("span", {"class":"serv_tit" }).get_text()
            lang =  r.find("span", {"class":"lang_tit" }).get_text()
            # No class or ID in this Element, so , use the index 2 to get it.
            quality = r.findChildren("span",recursive = False)[2].text
            item['download_links'].append({'server':server,'lang':lang,'quality':quality, 'link':link}) 

        item['subtitle_links'] = []
        listsub = soup.find("div", id= "list-sub")
        if listsub != None:
            rows = listsub.select('a[class*="lnk-lnk"]')
            for r in rows:
                link = r['href']
                if (link == None or link.strip() == ""):
                    continue
                server = r.find("span", {"class":"serv_tit" }).get_text()
                lang =  r.find("span", {"class":"lang_tit" }).get_text()            
                item['subtitle_links'].append({'server':server,'lang':lang,'link':link}) 

        item['cover_image_url'] = ''
        item['carousel_images'] = []
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
            item['image_urls'].append(imgSrc) # for dwonload
            item['carousel_images'].append(imgSrc) # image section without cover

        self.house_keeping_item(item,response)                
        return item



   