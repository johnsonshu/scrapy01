import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.womenadvancenc.org/2021/10/11/be-a-true-ally-this-indigenous-peoples-day/',
            'https://www.womenadvancenc.org/2021/10/07/were-still-on-facebook-and-instagram-and-heres-why/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.selector.xpath('//h1[@class="article__title  article__title--single"]/text()').get()
        # sometimes get garbled for single quote, if we don't use byte writing for file.
        with open("tutorial01.txt", 'ab') as f:  
            title += "\r\n"         
            f.write(title.encode())