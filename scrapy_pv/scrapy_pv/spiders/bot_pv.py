# -*- coding: utf-8 -*-
import urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest
from scrapy_pv.items import ScrapyPvItem
import string
import math
import socket

class BotPvSpider(CrawlSpider):
    name = 'bot_pv'
    allowed_domains = ['plazavea.com.pe']
    start_urls = ['http://www.plazavea.com.pe/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="nav"]/div/ul/li/a', deny=('/busca/'), ),
             callback='parse_grupo'),
    )

    def parse_grupo(self, response):
        # self.log("ENTRO PARSE 1:%s" % response.url)
        meta = response.xpath('//section[@class="main-departament"]/*/*/a[1]/@href')
        for m in meta:
            url = urlparse.urljoin(response.url, m.extract())
            # self.log("ENTRO BUCLE PARSE 1: %s" % url)
            # Seleccionamos la direccion
            yield SplashRequest(
                url,
                self.parse_prev_lista,
                endpoint='render.html',
                args={
                    'wait': 3,
                    'timeout': 60,
                }
            )

    def parse_prev_lista(self, response):
        #encuentro el script del "buscapagina"
        vscript = response.xpath('//div[@class="vitrine resultItemsWrapper"]/script/text()')[0].extract()
        #Obtengo la ruta de la categoria
        ruta = vscript[string.find(vscript,"/buscapagina?fq="):string.find(vscript, "&PageNumber='") + 12]
        #obtengo el numero de resultados
        meta = response.xpath('//span[@class="resultado-busca-numero"]/span[2]/text()')
        cant_pag = int(math.ceil(float(meta[0].extract()) / 12))
        #self.log("Numero Resultado: %s " % str(cant_pag))
        #Recorro la ruta de acuerdo a la cantidad de resultados
        i=1
        url = urlparse.urljoin(response.url, ruta)
        while i <= cant_pag:
            url_pag = url + str(i)
            i = i + 1
            #llamo a la funcion del parse item
            yield SplashRequest(
                url_pag,
                self.parse_lista,
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                    'wait': 0.5,
                    'images': 1,
                    'timeout': 60,
                }
            )
            #self.log("URL PAG.:%s" % url_pag)

    def parse_lista(self, response):
        #self.log("ENTRO:%s" % response.url)
        meta = response.xpath('//a[@class="prateleira__image-link"]/@href')
        for m in meta:
            #self.log("URL: %s" % url_item)
            yield SplashRequest(
                m.extract(),
                self.parse_item,
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                    'wait': 0.5,
                    'images':1,
                    'timeout': 60,
                }
            )

    def parse_item(self, response):
        default =ScrapyPvItem()
        default['principal'] = ['']
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
        default['url'] = ['']
        default['project'] = ['']
        default['spider'] = ['']
        default['server'] = ['']
        l = ItemLoader(item=default, response=response)

        l.add_xpath('principal', '//div[@class="bread-crumb"]/div/ul/li[1]/a/text()',
                    MapCompose(unicode.strip, unicode.title) )
        l.add_xpath('categoria', '//div[@class="bread-crumb"]/div/ul/li[2]/a/text()',
                    MapCompose(unicode.strip, unicode.title) )
        l.add_xpath('subcategoria', '//div[@class="bread-crumb"]/div/ul/li[3]/a/text()',
                    MapCompose(unicode.strip, unicode.title) )
        l.add_xpath('tipo', '//div[@class="bread-crumb"]/div/ul/li[4]/a/text()',
                    MapCompose(unicode.strip, unicode.title) )
        l.add_xpath('titulo', '//div[@class="product-name"]/div/text()',
                    MapCompose(unicode.strip, unicode.title) )
        l.add_xpath('brand', '//div[@class="product-brand"]/div/a/text()',
                    MapCompose(unicode.strip, unicode.title) )
        l.add_xpath('codigo_producto', '//div[@class="product-ref"]/div/text()',
                    MapCompose(unicode.strip, unicode.title) )
        l.add_xpath('imagen', '//img[@id="image-main"]/@src',
                    MapCompose(unicode.strip, unicode.title) )
        l.add_xpath('estrellas', '//span[@id="spnRatingProdutoTop"]/text()',
                    MapCompose(unicode.strip, unicode.title) )
        l.add_xpath('especificacion', '//td[@class="value-field Tipo"]/text()',
                    MapCompose(unicode.strip, unicode.title) )
        l.add_xpath('mejor_precio', '//strong[@class="skuBestPrice"]/text()',
                    MapCompose(unicode.strip, unicode.title) )
        l.add_xpath('precio_normal', '//strong[@class="skuListPrice"]/text()',
                    MapCompose(unicode.strip, unicode.title) )


        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())

        return l.load_item()
