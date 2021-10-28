import os
import hashlib
from urllib.parse import urlparse
from scrapy.utils.python import to_bytes

from scrapy.pipelines.images import ImagesPipeline


class MyImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        # file_extension is with '.' char
        filename, file_extension = os.path.splitext(request.url)  
        image_guid = hashlib.sha256(to_bytes(request.url)).hexdigest()
        return image_guid[0:3] + "/" + image_guid[3:6] + "/" \
            + f'{image_guid}{file_extension}'
       