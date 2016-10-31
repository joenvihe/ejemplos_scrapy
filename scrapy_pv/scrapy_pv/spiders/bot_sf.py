# -*- coding: utf-8 -*-
import scrapy
import urlparse
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_pv.items import ScrapyPvItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
import socket
import math


class BotSfSpider(CrawlSpider):
    name = 'bot_sf'
    allowed_domains = ['francosupermercado.com']
    start_urls = ['http://www.francosupermercado.com/']
    #//*[@id="columnLeft"]/div/div[1]/div/div[2]/ul/li[1]/div/a/div/text()
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="categories"]/li/div/a'),
             callback='parse_grupo'),
    )

    def parse_grupo(self, response):
        meta = response.xpath('//ul[@class="categories"]/li/div/div/a/@href')
        for m in meta:
            url = urlparse.urljoin(response.url, m.extract())
            yield scrapy.Request(url,
                                 self.parse_prev_lista
                                 )
            """
            yield SplashRequest(
                url,
                self.parse_prev_lista,
                endpoint='render.html',
                args={
                    'wait': 3,
                    'timeout': 60,
                }
            )
            """



    def parse_prev_lista(self, response):
        # obtengo el numero de resultados
        meta = response.xpath('//div[@class="fl_left result_left"]/span/span/strong/text()')
        cant_pag = int(math.ceil(float(meta[0].extract()) / 6))
        # self.log("Numero Resultado: %s " % str(cant_pag))
        # Recorro la ruta de acuerdo a la cantidad de resultados
        for j in range(cant_pag):
            #self.log(url + str(j+1))
            yield scrapy.Request(response.url + "&sort=2a&page=" + str(j+1),
                                 self.parse_lista
                                 )
        """
        i = 1
        while i <= cant_pag:
            url_pag = response.url + "&sort=2a&page=" + str(i)
            i = i + 1
            # llamo a la funcion del parse item
            yield SplashRequest(
                url_pag,
                self.parse_lista,
                endpoint='render.html',
                args={
                    'har': 1,
                    'html': 1,
                    'wait': 0.5,
                    'images': 1,
                    'timeout': 60,
                }
            )
        """

    def parse_lista(self, response):
        # self.log("ENTRO:%s" % response.url)
        meta = response.xpath('//div[@class="prods_padd"]/h2/span/a/@href')
        for m in meta:
            yield scrapy.Request(m.extract(),
                                 self.parse_item
                                 )
            # self.log("URL: %s" % url_item)
            """
            yield SplashRequest(
                m.extract(),
                self.parse_item,
                endpoint='render.html',
                args={
                    'har': 1,
                    'html': 1,
                    'wait': 0.5,
                    'images': 1,
                    'timeout': 60,
                }
            )
            """

    def parse_item(self, response):
        default = ScrapyPvItem()
        default['principal'] = ['super_franco']
        default['categoria'] = ['']
        default['subcategoria'] = ['']
        default['tipo'] = ['']
        default['titulo'] = ['']
        default['brand'] = ['']
        default['codigo_producto'] = ['']
        default['imagen'] = ['']
        default['estrellas'] = ['']
        default['especificacion'] = ['']
        default['mejor_precio'] = ['']
        default['precio_normal'] = ['']
        default['unidad'] = ['']
        default['promocion'] = ['']
        default['url'] = ['']
        default['project'] = ['']
        default['spider'] = ['']
        default['server'] = ['']
        l = ItemLoader(item=default, response=response)

        l.add_xpath('categoria', '//*[@id="bodyContent"]/div[1]/a[3]/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('subcategoria', '//*[@id="bodyContent"]/div[1]/a[4]/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('titulo', '//div[@class="info"]/h2[1]/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('codigo_producto', '//*[@id="bodyContent"]/div[1]/a[5]/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('imagen', '//a[@class="prods_pic_bg"]/img/@src',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('mejor_precio', '//span[@class="productSpecialPrice"]/text()',
                    MapCompose(unicode.strip, unicode.title))

        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())

        return l.load_item()
