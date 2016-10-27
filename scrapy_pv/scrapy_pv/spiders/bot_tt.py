# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy_pv.items import ScrapyPvItem
from scrapy.loader.processors import MapCompose
import socket

class BotTtSpider(CrawlSpider):
    name = 'bot_tt'
    allowed_domains = ['tottus.com.pe']
    start_urls = ['http://www.tottus.com.pe/tottus/productListFragment?']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@id="next"]')),
        Rule(LinkExtractor(restrict_xpaths='//div[@class=" item-product-caption"]/div/div[@class="title"]/a'),
             callback='parse_item')
    )

    def parse_item(self, response):
        default = ScrapyPvItem()
        default['principal'] = ['tottus']
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

        l.add_xpath('categoria', '//div[@class="title-category-section breadcrumb-nav"]/h3/a[1]/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('subcategoria', '//div[@class="title-category-section breadcrumb-nav"]/h3/a[2]/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('tipo', '//div[@class="title-category-section breadcrumb-nav"]/h3/text()[3]',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('titulo','//div[@class="item-product-caption product-detail"]/div/div/div[@class="title"]/h5/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('brand', '//div[@class="item-product-caption product-detail"]/div/div/div[@class="title"]/h5/span/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('imagen', '//div[@class="item-product-caption product-detail"]/div/div/img/@src',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('especificacion', '//div[@class="item-product-caption product-detail"]/div/div/div[@class="offer-details"]/div/span[2]/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('mejor_precio', '//div[@class="price-selector"]/div/span/span/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('unidad', '//div[@class="item-product-caption product-detail"]/div[@class="row"]/div[2]/div[@class="statement"]/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('promocion', '//div[@class="item-product-caption product-detail"]/div/div/div[@class="offer-details"]/div/span[1]/text()',
                    MapCompose(unicode.strip, unicode.title))

        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())

        return l.load_item()
