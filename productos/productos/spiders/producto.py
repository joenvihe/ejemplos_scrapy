# -*- coding: utf-8 -*-
import urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest
from productos.items import ProductosItem


class ProductoSpider(CrawlSpider):
    name = 'producto'
    allowed_domains = ['plazavea.com.pe']
    start_urls = ['http://www.plazavea.com.pe/']

    rules = (
       Rule(LinkExtractor(restrict_xpaths='//div[@class="nav"]/div/ul/li/a', deny=('/busca/'), ),callback='parse_grupo'),
    )

    def parse_grupo(self, response):
        #self.log("ENTRO PARSE 1:%s" % response.url)
        meta = response.xpath('//section[@class="main-departament"]/*/*/a[1]/@href')
        for m in meta:
            url = urlparse.urljoin(response.url, m.extract())
            #self.log("ENTRO BUCLE PARSE 1: %s" % url)
            i=1
            while i < 5:
                # cambiamos 12 por 50
                url_link = url[:-2] + "50#" + str(i)
                yield SplashRequest(
                    url_link,
                    self.parse_lista,
                    endpoint='render.html',
                    args={
                        'wait': 3,
                        'timeout':60,
                    }
                )
                i = i + 1


    def pagina_existe(self,response):
        #self.log("UNO:")
        if response.xpath('//a[@class="prateleira__image-link"]/@href'):
            self.log("URL: lleno")
            return True
        else:
            self.log("URL: vacio")
            return False
        #response.xpath('//a[@class="prateleira__image-link"]/@href').meta
        return False

    def parse_lista(self, response):
        self.log("RESPONSE URL :%s" % response.url)
        #self.log("RESPONSE %s" % response.xpath('//a[@class="prateleira__image-link"]/@href'))
        if self.pagina_existe(response):
            yield SplashRequest(
                response.url,
                self.parse_lista_item,
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                    'wait': 0.5,
                    'images':1,
                    'timeout':60.0,
                }
            )
        #self.log("Response:%s" % response.data['html'])


    def parse_lista_item(self, response):
        #self.log("ENTRO:%s" % response.url)
        meta = response.xpath('//a[@class="prateleira__image-link"]/@href')
        for m in meta:
            url_item = m.extract()
            #self.log("URL: %s" % url_item)
            yield SplashRequest(
                url_item,
                self.parse_item,
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                    'wait': 0.5,
                    'images':1,
                    'timeout':60.0,
                }
            )

    def parse_item(self, response):
        #self.log("ENTRO PARSE ITEM:%s" % response.url)
        #self.log("titulo: %s" % response.xpath('//div[@class="product-name"]/div/text()').extract())
        #self.log("brand: %s" % response.xpath('//div[@class="product-brand"]/div/a/text()').extract())
        #self.log("product_reference: %s" % response.xpath('//div[@class="product-ref"]/div/text()').extract())
        l = ItemLoader(item=ProductosItem(), response=response)

        l.add_xpath('titulo', '//div[@class="product-name"]/div/text()',
                    MapCompose(unicode.strip, unicode.title) )
        l.add_xpath('brand', '//div[@class="product-brand"]/div/a/text()',
                    MapCompose(unicode.strip, unicode.title) )
        l.add_xpath('product_reference', '//div[@class="product-ref"]/div/text()',
                    MapCompose(unicode.strip, unicode.title) )

        """
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        self.log("tit   le: %s" % response.xpath('//*[@itemprop="name"][1]/text()').extract())
        self.log("price: %s" % response.xpath('//*[@itemprop="price"][1]/text()').re('[.0-9]+'))
        self.log("description: %s" % response.xpath('//*[@itemprop="description"][1]/text()').extract())
        self.log("address: %s" % response.xpath('//*[@itemtype="http://schema.org/Place"][1]/text()').extract())
        self.log("image_urls: %s" % response.xpath('//*[@itemprop="image"][1]/@src').extract())
        """
        return l.load_item()