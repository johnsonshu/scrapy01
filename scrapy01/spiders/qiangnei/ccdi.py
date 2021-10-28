import datetime
import socket
import scrapy

from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor

from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.http import Request

from scrapy01.items import CommonItem
from scrapy01.spiders.zc2tech import Zc2techSpider

# https://www.ccdi.gov.cn/
# 中纪委

class CcpiSpider(Zc2techSpider):
    name = 'ccpi'

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy01.pipelines.ccpi.CcpiPipeline': 300,
            'scrapy01.pipelines.myimage.MyImagesPipeline': 1
            # 'scrapy.pipelines.images.ImagesPipeline': 1
        },
        'IMAGES_STORE' : 'file_image/ccpi',
        'FILES_STORE'  : 'file_image/ccpi',        
        
    }

    allowed_domains = ['www.ccdi.gov.cn']
    start_urls = ['https://www.ccdi.gov.cn/']

    rules = (
        # 要闻，评论的话，就要取具体内容了，所以 deny
        Rule(LinkExtractor(deny=(r'/yaowen/\d{6}',r'/pl/\d{6}',r'/toutu/\d{6}')),follow=True),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=(r'/[a-z]+/\d{6}/\d{8}_\d+\.html', )), callback='parse_item'),
    )

    def parse(self, response):
        for link in self.link_extractor.extract_links(response):
            yield Request(link.url, callback=self.parse)

    def parse_item(self, response):
        item = CommonItem()
        #item['id'] = response.xpath('//div[@class="flater_tab"]/div/h2/text()').re(r'ID: (\d+)')
        item['title'] = response.xpath('//div[@class="flater_tab"]/div/h2/text()').get()

        strPub =  response.xpath('//div[@class="daty_con"]/em/text()').get()
        if strPub != None :
            # split with full-widht colon '：'
             item['pub_time'] = strPub.split("：")[-1]
  
        item['article'] = response.xpath('//div[@class="TRS_Editor"]/node()').get()
  
        #images
        imageNodes = response.xpath('//div[@class="content"]//img').getall()
        
        item['image_urls'] = []

        for img in imageNodes:
            imgSrc = Selector(text=img).xpath('//img/@src').get()            
            item['image_urls'].append(imgSrc)

        self.house_keeping_item(item,response)                
        return item

        # url = response.xpath('//td[@id="additional_data"]/@href').get()
        # return response.follow(url, self.parse_additional_page, cb_kwargs=dict(item=item))

    # def parse_additional_page(self, response, item):
    #     item['additional_data'] = response.xpath('//p[@id="additional_data"]/text()').get()
    #     return item
       


   