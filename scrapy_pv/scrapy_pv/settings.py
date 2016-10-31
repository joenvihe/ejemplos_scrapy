# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_pv project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapy_pv'

SPIDER_MODULES = ['scrapy_pv.spiders']
NEWSPIDER_MODULE = 'scrapy_pv.spiders'

DOWNLOADER_MIDDLEWARES = {
    # Engine side
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    # Downloader side
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
#Splash server address
SPLASH_URL = 'http://192.168.99.100:8050/'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapy_pv (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'scrapy_pv.pipelines.mysql.MysqlWriter': 700,
}

#MYSQL_PIPELINE_URL = 'mysql://root:pass@mysql:3306/productos'
#MYSQL_PIPELINE_URL = 'mysql://root:pass@127.0.0.1:3306/productos'
#MYSQL_PIPELINE_URL = 'mysql://root:pass@127.0.0.1:3306/productos2'
MYSQL_PIPELINE_URL = 'mysql://root:pass@127.0.0.1:3306/productos'
LOG_ENABLED = True
DOWNLOAD_DELAY = 0.5    # 250 ms of delay
COOKIES_ENABLED = True
#COOKIES_DEBUG = True

#scrapeando cortesmente
USER_AGENT = 'JOENVIHE-validando precios (enrique@vicenteh.com)'
CONCURRENT_REQUESTS_PER_DOMAIN = 32 # request concurrentes
CONCURRENT_REQUESTS = 64 # request maximos
#AUTOTHROTTLE_ENABLED = True # regula la cantidad de request
#HTTPCACHE_ENABLED = True # verificar el cache por dia?
#HTTPCACHE_EXPIRATION_SECS = 86400 # expira el cache en 24 horoas, el tiempo es expresado en segundos