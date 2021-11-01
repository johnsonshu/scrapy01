# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


def serialize_images(value):
    return f'$ {str(value)}'

class CommonItem(Item):
    # Primary fields
    title = Field()
    article = Field()
    description = Field()
    info_html = Field()
    cover_image_url = Field()
    carousel_images = Field()
    image_urls = Field()
    image_dl_results = Field()

    # Housekeeping fields
    meta_url = Field()
    meta_project = Field()
    meta_spider = Field()
    meta_server = Field()
    meta_date = Field()

class YifyMoviesItem(CommonItem):
    download_links = Field()
    subtitle_links = Field()
  