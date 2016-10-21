# -*- coding: utf-8 -*-
"""
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from splash.items import SplashItem
"""


import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
import json
from scrapy.http.headers import Headers

class DmozSpider(scrapy.Spider):
    name = 'dmoz'
    allowed_domains = ['dmoz.org']
    start_urls = ['http://www.dmoz.org/']

    # http_user = 'splash-user'
    # http_pass = 'splash-password'

    def parse(self, response):
        le = LinkExtractor()
        for link in le.extract_links(response):

            self.log(link.url)
            yield SplashRequest(
                link.url,
                self.parse_link,
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                }
            )


    def parse_link(self, response):
        self.log("PARSED %s" % response.url)
        self.log("TITULO %s " % response.css("title").extract())
        self.log("TITULO %s " % response.data["har"]["log"]["pages"])
        self.log("TITULO %s " % response.headers.get('Content-Type'))
"""
body = json.dumps({"url": link.url, "wait": 0.5}, sort_keys=True)
headers = Headers({'Content-Type': 'application/json'})
yield scrapy.Request(RENDER_HTML_URL, callback=self.parse_link, method="POST",
                     body=body, headers=headers)
"""
"""
print(response.css("title").extract())
print(response.data["har"]["log"]["pages"])
print(response.headers.get('Content-Type'))
"""
