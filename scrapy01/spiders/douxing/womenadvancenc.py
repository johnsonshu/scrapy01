import datetime
import socket
import scrapy

from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.selector import Selector

from scrapy01.items import CommonItem


class EasySpider(CrawlSpider):
    name = 'womenadvancenc'
    #allowed_domains = ["womenadvancenc.org"]

# from scrapy.pipelines.images import ImagesPipeline
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy01.pipelines.base.MongoPipeline': 300,
            'scrapy01.pipelines.myimage.MyImagesPipeline': 1
            # 'scrapy.pipelines.images.ImagesPipeline': 1
        },
        'IMAGES_STORE' : 'file_image/wo/womenadvancenc',
        'FILES_STORE'  : 'file_image/wo/womenadvancenc',
        
    }

    # Start on the first index page
    start_urls = ['https://www.womenadvancenc.org/page/2/']

    # Rules for horizontal and vertical crawling
    
    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths='//*[contains(@class,"next")]')),
    #     Rule(LinkExtractor(restrict_xpaths='//div[@class="article__title  article--thumb__title"]/@href'),
    #     callback='parse_item')
    # )

    def start_requests(self):
        urls = [
            'https://www.womenadvancenc.org/page/2/',
            'https://www.womenadvancenc.org/page/3/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_article_list)

    def parse_article_list(self,response):
        xpath_list = response.xpath("//div[@class='article__title  article--thumb__title']/a/@href").getall()
        for entry in xpath_list:
            yield scrapy.Request(url=entry, callback=self.parse)
       

    def parse(self, response):
        item = CommonItem()
        #item['id'] = response.xpath('//div[@class="flater_tab"]/div/h2/text()').re(r'ID: (\d+)')
        item['title'] = response.xpath('//h1[contains(@class,"article__title")]/text()').get()
        #pNodes = response.xpath('//article[contains(@class,"post-article")]/p/node()').getall()
        pNodes = response.xpath('//article[contains(@class,"post-article")]/p').getall()
        item['article'] = ' '.join([n for n in pNodes])

        #images
        imageNodes = response.xpath('//article[contains(@class,"post-article")]//img[contains(@class,"wp-image-")]').getall()
        
        item['image_urls'] = []

        for img in imageNodes:
            imgSrc = Selector(text=img).xpath('//img/@src').get()
            # Sample:'https://www.womenadvancenc.org/wp-content/uploads/2021/08/screen-shot-2021-08-11-at-12.26.39-pm-e1628701296235-300x97.png'
            if r"/wp-content/uploads/" not in imgSrc:
                continue
            
            item['image_urls'].append(imgSrc)

            # It's OK that the value is None
            imgSrcSet = Selector(text=img).xpath('//img/@srcset').get()            
            if imgSrcSet != None :
                imgUrls = imgSrcSet.split(',')
                for url in imgUrls:
                    # Get the URL part, throw out size info part
                    s = url.strip().split(' ')[0].strip()
                    if s.startswith("http") :
                        item['image_urls'].append(s)

        return item

