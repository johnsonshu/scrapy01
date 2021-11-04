# Scrapy settings for scrapy01 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from shutil import which

import scrapy

LOG_LEVEL = 'INFO'
LOG_STDOUT = False
BOT_NAME = 'iroha-dev'

SELENIUM_DRIVER_NAME = 'firefox'
#SELENIUM_DRIVER_EXECUTABLE_PATH = r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
SELENIUM_DRIVER_EXECUTABLE_PATH = which('geckodriver')
SELENIUM_DRIVER_ARGUMENTS=['--headless'] 

SPIDER_MODULES = ['scrapy01.spiders']
NEWSPIDER_MODULE = 'scrapy01.spiders'

#DOWNLOADER_CLIENTCONTEXTFACTORY = 'scrapy01.custom.contexts.CustomContextFactory'
DOWNLOADER_CLIENT_TLS_METHOD = 'TLSv1.2'
DOWNLOADER_CLIENT_TLS_VERBOSE_LOGGING = True

GLOBAL_PROXY = 'cn-proxy.jp.XXXX.com:80'

DOWNLOADER_MIDDLEWARES = {
    'scrapy01.middlewares.CustomProxyMiddleware' : 1,
    'scrapy01.middlewares.MySeleniumMiddleware' :101,
}

# IMAGES_STORE = "download_images"
# FILES_STORE  = "download_files"

# FILES_URLS_FIELD = 'file_urls'
# FILES_RESULT_FIELD = 'files'

IMAGES_URLS_FIELD = 'image_urls'
IMAGES_RESULT_FIELD = 'image_dl_results'

CLOSESPIDER_PAGECOUNT = 2
CLOSESPIDER_ITEMCOUNT = 2
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapy01 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapy01.middlewares.Scrapy01SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'scrapy01.middlewares.Scrapy01DownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
   'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     'scrapy01.pipelines.base.MongoPipeline': 300,
# }

MONGO_URI = 'ubuntu20-lts:27017'
MONGO_DATABASE = 'iroha-dev'
#MONGOLAB_USER = 'user_name'
#MONGOLAB_PASS = 'password'


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
