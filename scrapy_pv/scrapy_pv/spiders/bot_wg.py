# -*- coding: utf-8 -*-
import scrapy
import urlparse
from scrapy.loader import ItemLoader
from scrapy_pv.items import ScrapyPvItem
from scrapy.loader.processors import MapCompose
import socket

class BotWgSpider(scrapy.Spider):
    name = 'bot_wg'
    allowed_domains = ['wong.com.pe']
    #start_urls = ['https://www.wong.com.pe/FO/supermercados/index.go?search=2&caip=1']
    start_urls = ['https://www.wong.com.pe/FO/supermercados/index.go?search=2&caip=1']
    #https://www.wong.com.pe/FO/supermercados/productos.go?idCategoria=3962&idSubCategoria=4207
    #https://www.wong.com.pe/FO/fichas/index.go?idprod=143229&cat=4089

    def start_requests(self):
        # https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#cookies-debug
        # Multiple cookie sessions per spider
        for i,url in enumerate(self.start_urls):
            yield scrapy.Request(url,
                                 self.parse,
                                 method='POST',
                                 meta={'cookiejar': i}
                                 )

    def parse(self, response):
        # Get item URLs and yield Requests
        meta = response.xpath('//li[@class="subcategoria"]/a/@id')
        for m in meta:
            ids=m.extract().split("_") # dividimos la categoria de la subcategoria
            url="https://www.wong.com.pe/FO/supermercados/productos.go?idCategoria="+ids[0]+"&idSubCategoria="+ids[1]
            yield scrapy.Request(urlparse.urljoin(response.url, url),
                                 self.parse_lista,
                                 meta={'cookiejar': response.meta['cookiejar']}
                                 )

    def parse_lista(self, response):
        s_text = " ".join(response.xpath('//div[@id="breadcrumbs"]/text()').extract()[1].split())
        a_categ = s_text.split("/")
        meta = response.xpath('//tbody/tr/@id')
        for m in meta:
            ids = m.extract().split("_")  # dividimos y obtenermos el cod del producto
            url="https://www.wong.com.pe/FO/fichas/index.go?idprod="+ids[1]
            yield scrapy.Request(urlparse.urljoin(response.url, url),
                                 self.parse_item,
                                 meta={'cookiejar': response.meta['cookiejar'],
                                       'v_categoria':a_categ[0],
                                       'v_subcategoria': a_categ[1],
                                       'v_id': ids[1]
                                       }
                                 )

    def parse_item(self,response):
            default = ScrapyPvItem()
            default['principal'] = ['wong']
            default['categoria'] = [response.meta['v_categoria']]
            default['subcategoria'] = [response.meta['v_subcategoria']]
            default['tipo'] = ['']
            default['titulo'] = ['']
            default['brand'] = ['']
            default['codigo_producto'] = [response.meta['v_id']]
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

            l.add_xpath('tipo', '//*[@id="f_productos_0"]/span[1]/text()',
                        MapCompose(unicode.strip, unicode.title))
            l.add_xpath('titulo', '//*[@id="f_productos_0"]/span[3]/text()',
                        MapCompose(unicode.strip, unicode.title))
            l.add_xpath('brand', '//*[@id="f_productos_0"]/span[2]/text()',
                        MapCompose(unicode.strip, unicode.title))
            l.add_xpath('imagen', '//*[@id="foto"]/img/@src',
                        MapCompose(unicode.strip, unicode.title))
            l.add_xpath('mejor_precio', '//*[@id="f_productos_0"]/span[4]/text()',
                        MapCompose(unicode.strip, unicode.title))
            l.add_xpath('precio_normal', '//*[@id="f_productos_0"]/span[3]/span/text()',
                        MapCompose(unicode.strip, unicode.title))

            l.add_value('url', response.url)
            l.add_value('project', self.settings.get('BOT_NAME'))
            l.add_value('spider', self.name)
            l.add_value('server', socket.gethostname())

            return l.load_item()
